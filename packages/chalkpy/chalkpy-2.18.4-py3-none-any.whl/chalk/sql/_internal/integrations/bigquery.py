from __future__ import annotations

import contextlib
import logging
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import pyarrow as pa

from chalk.features import FeatureConverter
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from google.cloud.bigquery import ScalarQueryParameterType
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.BINARY,
        sa.BLOB,
        sa.LargeBinary,
        sa.Float,
        sa.Integer,
        sa.Time,
        sa.String,
        sa.Text,
        sa.VARBINARY,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )


def _compile_parameter_to_bq_scalar_type(primitive: Any) -> ScalarQueryParameterType:
    # gated by import check in caller
    from google.cloud.bigquery import SqlParameterScalarTypes

    if isinstance(primitive, bool):
        return SqlParameterScalarTypes.BOOLEAN
    elif isinstance(primitive, int):
        return SqlParameterScalarTypes.INT64
    elif isinstance(primitive, float):
        return SqlParameterScalarTypes.FLOAT64
    elif isinstance(primitive, str):
        return SqlParameterScalarTypes.STRING
    elif isinstance(primitive, datetime):
        return SqlParameterScalarTypes.DATETIME
    elif isinstance(primitive, date):
        return SqlParameterScalarTypes.DATE
    elif isinstance(primitive, Decimal):
        return SqlParameterScalarTypes.DECIMAL
    elif isinstance(primitive, time):
        return SqlParameterScalarTypes.TIME
    elif isinstance(primitive, bytes):
        return SqlParameterScalarTypes.BYTES
    else:
        raise TypeError(f"Unsupported BigQuery parameter type '{type(primitive)}'")


_logger = get_logger(__name__)


class BigQuerySourceImpl(BaseSQLSource):
    kind = SQLSourceKind.bigquery

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[str] = None,
        location: Optional[str] = None,
        credentials_base64: Optional[str] = None,
        credentials_path: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            import sqlalchemy_bigquery
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")
        del sqlalchemy_bigquery  # unused
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        self.location = location or load_integration_variable(integration_name=name, name="BQ_LOCATION")
        self.dataset = dataset or load_integration_variable(integration_name=name, name="BQ_DATASET")
        self.project = project or load_integration_variable(integration_name=name, name="BQ_PROJECT")
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_BASE64"
        )
        self.credentials_path = credentials_path or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_PATH"
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def get_sqlglot_dialect(self) -> str | None:
        return "bigquery"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in {
                "location": self.location,
                "credentials_base64": self.credentials_base64,
                "credentials_path": self.credentials_path,
            }.items()
            if v is not None
        }
        return URL.create(drivername="bigquery", host=self.project, database=self.dataset, query=query)

    @contextlib.contextmanager
    def _get_bq_client(self):
        # gated already
        import google.cloud.bigquery
        import google.cloud.bigquery.dbapi

        with self.get_engine().connect() as conn:
            dbapi = conn.connection.dbapi_connection
            assert isinstance(dbapi, google.cloud.bigquery.dbapi.Connection)
            client = dbapi._client
            assert isinstance(client, google.cloud.bigquery.Client)
            yield client

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Connection],
        polars_read_csv: bool = False,
    ) -> pa.Table:
        try:
            try:
                from google.cloud import bigquery
                from sqlalchemy.sql import Select
            except ModuleNotFoundError:
                raise missing_dependency_exception("chalkpy[bigquery]")

            if isinstance(finalized_query.query, Select):
                validate_dtypes_for_efficient_execution(
                    finalized_query.query, _supported_sqlalchemy_types_for_pa_querying
                )

            assert len(finalized_query.temp_tables) == 0, "Should not create temp tables with bigquery source"

            with self._get_bq_client() as client:
                try:
                    sql, positional_params, named_params = self.compile_query(finalized_query)
                    query_parameters = [
                        # TODO: Consider type_ parameter more carefully.
                        bigquery.ScalarQueryParameter(
                            name=name, value=value, type_=_compile_parameter_to_bq_scalar_type(value)
                        )
                        for name, value in (named_params.items() if isinstance(named_params, dict) else named_params)
                    ]
                    job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
                    res = client.query(sql, job_config=job_config)
                    table = res.to_arrow()
                    converters = columns_to_converters(table.column_names)

                    schema = pa.schema(
                        [
                            pa.field(k, converters[k].pyarrow_dtype)
                            if k in converters
                            else pa.field(k, table.schema.field_by_name(k))
                            for k in table.column_names
                        ]
                    )

                    # n.b. this needs to become a pa_cast
                    pa_table = table.cast(schema)

                    return pa_table
                finally:
                    client.close()
        except Exception as e:
            _logger.error(
                f"Failed to execute BigQuery query efficiently. Query: {finalized_query.query=}, {finalized_query.params=}",
                exc_info=e,
            )
            raise UnsupportedEfficientExecutionError(
                "Failed to execute BigQuery query via pyarrow, falling back to sqlalchemy.", log_level=logging.WARNING
            )
