from __future__ import annotations

import contextlib
import datetime as dt
import io
import logging
import os
import uuid
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Mapping, Optional, Type, Union

import pyarrow as pa
import pyarrow.parquet as pq

import chalk.logging
from chalk.features import FeatureConverter
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.integrations.util import convert_hex_to_binary, json_parse_and_cast
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import is_binary_like
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import boto3
    from mypy_boto3_s3 import S3Client
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL
    from sqlalchemy.types import TypeEngine

_logger = get_logger(__name__)
_public_logger = chalk.logging.chalk_logger


def get_supported_redshift_unload_types() -> List[Type["TypeEngine"]]:
    """
    This is a method instead of a constant to avoid import issues
    :return:
    """

    import sqlalchemy as sa

    return [
        sa.JSON,
        sa.ARRAY,
        sa.REAL,
        sa.FLOAT,
        sa.NUMERIC,
        sa.DECIMAL,
        sa.INTEGER,
        sa.SMALLINT,
        sa.BIGINT,
        sa.TIMESTAMP,
        sa.DATETIME,
        sa.DATE,
        sa.TIME,
        sa.TEXT,
        sa.CLOB,
        sa.VARCHAR,
        sa.NVARCHAR,
        sa.CHAR,
        sa.NCHAR,
        sa.BLOB,
        sa.BINARY,
        # sa.VARBINARY, # This dtype is not supported for UNLOAD into PARQUET
        sa.BOOLEAN,
    ]


_DEFAULT_REDSHIFT_S3_CLIENT = None


class RedshiftSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.redshift

    def __init__(
        self,
        host: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        s3_client: S3Client = None,
        s3_bucket: str = None,
    ):
        try:
            import boto3
            import redshift_connector
        except ImportError:
            raise missing_dependency_exception("chalkpy[redshift]")
        del redshift_connector
        self.host = host or load_integration_variable(name="REDSHIFT_HOST", integration_name=name)
        self.db = db or load_integration_variable(name="REDSHIFT_DB", integration_name=name)
        self.user = user or load_integration_variable(name="REDSHIFT_USER", integration_name=name)
        self.password = password or load_integration_variable(name="REDSHIFT_PASSWORD", integration_name=name)
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(name="REDSHIFT_PORT", integration_name=name, parser=int)
        )
        # TODO customer may want to provide the s3 creds via the "AWS Integration" we provide.
        # NOTE: Chalk Engine injects its own S3 client via `_DEFAULT_REDSHIFT_S3_CLIENT`
        self._s3_client = s3_client or _DEFAULT_REDSHIFT_S3_CLIENT or boto3.client("s3")
        self._s3_bucket = s3_bucket or load_integration_variable(
            name="REDSHIFT_UNLOAD_S3_BUCKET", integration_name=name
        )
        if self._s3_bucket is not None:
            self._s3_bucket = self._s3_bucket.removesuffix("s3://").lstrip("/")
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def convert_db_types(self, value: Any, converter: FeatureConverter):
        """
        Redshift returns binary data as a hex string. Need to convert to bytes before returning as feature data.
        """
        if is_binary_like(converter.pyarrow_dtype):
            assert isinstance(value, str)
            value = bytes.fromhex(value)
        return super().convert_db_types(value, converter)

    def get_sqlglot_dialect(self) -> str | None:
        return "redshift"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="redshift+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
            port=self.port,
        )

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Connection],
        polars_read_csv: bool = False,
    ) -> pa.Table:
        def _do_query():
            with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
                with cnx.begin():
                    cursor = cnx.connection.cursor()
                    compiled_statement = self._get_compiled_query(finalized_query)

                    from sqlalchemy.sql import Select

                    if isinstance(finalized_query.query, Select):
                        validate_dtypes_for_efficient_execution(
                            finalized_query.query, supported_types=get_supported_redshift_unload_types()
                        )
                    execution_context = self.get_engine().dialect.execution_ctx_cls._init_compiled(  # type: ignore
                        connection=cnx,
                        dialect=cnx.dialect,
                        dbapi_connection=cnx.connection.dbapi_connection,
                        execution_options={},
                        compiled=compiled_statement,
                        parameters=[],
                        invoked_statement=None,
                        extracted_parameters=None,
                    )
                    assert isinstance(execution_context, self.get_engine().dialect.execution_ctx_cls)
                    operation = execution_context.statement
                    assert operation is not None
                    params = execution_context.parameters[0]
                    unload_destination = None
                    started_at = dt.datetime.now(dt.timezone.utc)

                    # Redshift requires that the query used for an unload statement is literal quoted. That means that we CANNOT use a bind parameters within it
                    # So, we will get around this using a "CREATE TEMP TABLE as SELECT (query with bind parameters)"
                    # Then, we will run an unload query without any parameters: UNLOAD ('select * from temp_table')
                    # Finally, we can drop the temp table
                    temp_table_name = f"query_{str(uuid.uuid4()).replace('-', '_')}"
                    try:
                        _logger.debug(f"Executing query & creating temp table '{temp_table_name}'")
                        cursor.execute(f"CREATE TEMP TABLE {temp_table_name} AS ({operation})", params)
                    except Exception as e:
                        raise RuntimeError(f"Failed to create temp table for operation: {operation}") from e
                    try:
                        unload_destination = f"{temp_table_name}/"
                        unload_uri = f"s3://{self._s3_bucket}/{unload_destination}"
                        unload_query = f"UNLOAD ('SELECT * FROM {temp_table_name}') TO '{unload_uri}' IAM_ROLE default FORMAT PARQUET EXTENSION 'parquet'"
                        _public_logger.info(f"Executing UNLOAD query: {unload_query}")
                        cursor.execute(unload_query)
                    finally:
                        cursor.execute(f"DROP TABLE {temp_table_name}")

                    finished_at = dt.datetime.now(dt.timezone.utc)
                    return started_at, finished_at, unload_destination

        try:
            started_at, finished_at, unload_destination = _do_query()
        except Exception as e:
            _public_logger.warn(
                f"Failed to run Redshift query with efficient execution, falling back to default execution mode.",
                exc_info=True,
            )
            raise UnsupportedEfficientExecutionError(
                f"Failed to run Redshift query with efficient execution, falling back to default execution mode: {e}",
                log_level=logging.INFO,
            ) from e
        # Redshift is case-insensitive with column names, so let's map it back to what we were expecting
        assert unload_destination is not None
        tables: list[pa.Table] = []

        for filename in _list_files(self._s3_client, self._s3_bucket, unload_destination):
            tables.append(_download_file_to_table(self._s3_client, self._s3_bucket, filename, columns_to_converters))
        if len(tables) == 0:
            # Attempt to infer schema from query fields
            results_schema = {k: v.converter.pyarrow_dtype for k, v in finalized_query.fields.items()}
            tbl = pa.Table.from_pydict({x: [] for x in results_schema}, pa.schema(results_schema))
        elif len(tables) == 1:
            tbl = tables[0]
        else:
            tbl = pa.concat_tables(tables, promote=False)  # No need to promote since we already casted

        return tbl


# TODO move chalkshared.utils.storage_client into chalkpy
def _list_files(client: "S3Client", bucket: str, prefix: str) -> Iterable[str]:
    try:
        continuation_token = None
        while True:
            if continuation_token is None:
                resp = client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                )
            else:
                resp = client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=continuation_token,
                )
            # If no keys returned, the server omits 'Contents'
            for row in resp.get("Contents", []):
                key = row.get("Key")
                assert key is not None, "all objects must have a key"
                yield key
            if not resp["IsTruncated"]:
                return
            continuation_token = resp["NextContinuationToken"]
    except Exception:
        _logger.error(f"Got exception while listing files for {prefix=}", exc_info=True)
        raise


def _download_file_to_table(
    client: "S3Client",
    bucket: str,
    filename: str,
    cols_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
):
    buffer = io.BytesIO()
    client.download_fileobj(Bucket=bucket, Key=filename, Fileobj=buffer)
    buffer.seek(0)
    tbl = pq.read_table(buffer)
    # TODO (CHA-2232) Delete the `filename` from the bucket since we'll never look at it again

    # Infer results schema from table columns & map to correct dtype
    converters = cols_to_converters(tbl.column_names)
    results_schema: Mapping[str, pa.DataType] = {col: converters[col].pyarrow_dtype for col in tbl.column_names}
    return json_parse_and_cast(tbl, results_schema)
