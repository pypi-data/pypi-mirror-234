from __future__ import annotations

import collections
import contextlib
import csv
import io
import logging
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Mapping, Optional, Sequence, Union

import pyarrow as pa
import pyarrow.csv

from chalk.features import FeatureConverter
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    TableIngestMixIn,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import URL, Connection

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_csv_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_csv_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.Float,
        sa.Integer,
        sa.String,
        sa.Text,
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

_logger = get_logger(__name__)


class PostgreSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.postgres

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            import psycopg  # Used for the async driver
            import psycopg2  # Used for the sync driver
            import sqlalchemy.dialects
            import sqlglot
            import sqlglot.expressions
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        del psycopg  # unused
        if "postgresql.psycopg" not in sqlalchemy.dialects.registry.impls:
            sqlalchemy.dialects.registry.register(
                "postgresql.psycopg", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect"
            )
        if "postgresql.psycopg_async" not in sqlalchemy.dialects.registry.impls:
            sqlalchemy.dialects.registry.register(
                "postgresql.psycopg_async", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect_async"
            )
        self.name = name
        self.host = host or load_integration_variable(integration_name=name, name="PGHOST")
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(integration_name=name, name="PGPORT", parser=int)
        )
        self.db = db or load_integration_variable(integration_name=name, name="PGDATABASE")
        self.user = user or load_integration_variable(integration_name=name, name="PGUSER")
        self.password = password or load_integration_variable(integration_name=name, name="PGPASSWORD")
        self.ingested_tables: Dict[str, Any] = {}
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault("pool_size", 20)
        async_engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
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
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    def get_sqlglot_dialect(self) -> str | None:
        return "postgres"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg_async",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def _get_parsed_table_via_polars(
        self,
        finalized_query: FinalizedChalkQuery,
        connection: Optional[Connection],
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
    ) -> pyarrow.Table:
        import polars as pl

        buffer = self._get_result_csv_buffer(finalized_query, connection=connection, escape_char='"')
        first_line = buffer.readline()
        column_names = list(
            csv.reader(
                [first_line.decode("utf8")],
                doublequote=True,
                quoting=csv.QUOTE_MINIMAL,
            )
        )[0]
        buffer.seek(0)
        converters = columns_to_converters(column_names)

        parse_dtypes = {}
        boolean_columns = []
        date_columns = []
        datetime_col_to_dtype: Dict[str, pl.Datetime] = {}
        for col_name, converter in converters.items():
            dtype = converter.polars_dtype
            if dtype == pl.Boolean:
                # Parsing "t" and "f" as booleans fails.
                # We will parse the column as a string, and then
                # convert it to a boolean later.
                parse_dtypes[col_name] = pl.Utf8
                boolean_columns.append(col_name)
            elif dtype == pl.List:
                # We will parse the list as a string, and then
                # convert it to a list later. Polars does not
                # support parsing lists directly from CSV.
                parse_dtypes[col_name] = pl.Utf8
            elif dtype == pl.Datetime:
                # Parse as str, convert to datetime later.
                # It's important to parse datetimes as strings,
                # because `polars.read_csv()` just turns
                # unparseable datetimes into nulls, a huge no-no.
                parse_dtypes[col_name] = pl.Utf8
                # Make linter happy
                assert isinstance(dtype, pl.Datetime) or dtype == pl.Datetime
                datetime_col_to_dtype[col_name] = dtype
            elif dtype == pl.Date:
                # Parse as str, convert to date later.
                # It's important to parse dates as strings,
                # because `polars.read_csv()` just turns
                # unparseable dates into nulls, a huge no-no.
                parse_dtypes[col_name] = pl.Utf8
                date_columns.append(col_name)
            else:
                parse_dtypes[col_name] = dtype

        """
        CSV -> Polars -> Pyarrow table
        """
        # Previously we were using `pyarrow.csv.read_csv` but performance
        # degraded over time up till the next reboot.
        #
        # pl.read_csv(use_pyarrow=True) has the same performance degradation,
        # UNLESS a `dtypes` arg is provided.
        pl_table = pl.read_csv(buffer, dtypes=parse_dtypes)
        if boolean_columns:
            # DO NOT use map_dict. Causes a segfault when multiple uvicorn workers are handling
            # requests in parallel.
            boolean_when_mappings = [
                pl.when(pl.col(bool_col).is_null())
                .then(None)
                .otherwise(pl.col(bool_col) == "t")
                .cast(pl.Boolean)
                .alias(bool_col)
                for bool_col in boolean_columns
            ]
            pl_table = pl_table.with_columns(*boolean_when_mappings)
        if date_columns:
            for date_col in date_columns:
                pl_table = _get_df_with_parsed_dt_column(
                    pl_table=pl_table,
                    col_name=date_col,
                    parser_formats=["%Y-%m-%d", "%D", "%m/%d/%Y"],
                    target_dtype=pl.Date,
                )
        if datetime_col_to_dtype:
            for dt_col, dt_type in datetime_col_to_dtype.items():
                unit_to_precision = {
                    "ms": "%.3f",
                    "us": "%.6f",
                    "ns": "%.9f",
                }
                precision = unit_to_precision.get(dt_type.time_unit, "%.6f")
                dt_format = f"%Y-%m-%d %H:%M:%S{precision}"
                dt_format_with_tz = f"{dt_format}%#z"
                datetime_parser_formats = [dt_format, dt_format_with_tz, "%Y-%m-%d"]
                pl_table = _get_df_with_parsed_dt_column(
                    pl_table=pl_table,
                    col_name=dt_col,
                    parser_formats=datetime_parser_formats,
                    target_dtype=pl.Datetime,
                )

        parsed_table = pl_table.to_arrow()
        if len(converters) != len(parsed_table.column_names):
            _logger.warn(
                f"mismatch in number of columns between query and converters: {len(converters)=}, {len(parsed_table.column_names)=}"
            )

        """
        Pyarrow table -> Pyarrow table with correct dtype
        """
        # Cast to target pyarrow dtypes. Some of the columns may have been parsed with
        # the correct polars dtype and then cast to the correct pyarrow dtype, but
        # some other columns such as lists have intentionally not been cast.
        restricted_schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
        # Reorder columns to match order of the schema.
        return parsed_table.select([c for c in converters.keys()]).cast(restricted_schema)

    def _get_result_csv_buffer(
        self, finalized_query: FinalizedChalkQuery, connection: Optional[Connection], escape_char: str
    ) -> io.BytesIO:
        import psycopg2.sql

        stmt, positional_params, named_params = self.compile_query(finalized_query, paramstyle="named")
        assert len(positional_params) == 0, "should not have any positional params"

        # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects
        # Forcing quote so the unquoted empty string will represent null values
        stmt = _reformat_compiled_query_string_for_csv_output(
            stmt,
            escape_char=escape_char,
            named_params=named_params,
        )

        formatted_stmt = psycopg2.sql.SQL(stmt).format(
            **{k: psycopg2.sql.Literal(v) for (k, v) in named_params.items()}
        )
        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            dbapi = cnx.connection
            with dbapi.cursor() as cursor:
                buffer = io.BytesIO()
                cursor.copy_expert(formatted_stmt, buffer)
        buffer.seek(0)

        return buffer

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Connection],
        polars_read_csv: bool = False,
    ) -> pa.Table:
        from sqlalchemy.sql import Select

        if env_var_bool("CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION_WITHOUT_EXCEPTION"):
            raise UnsupportedEfficientExecutionError(
                (
                    f"The SQL statement will be executed into SQLAlchemy objects, as the environment "
                    "variable 'CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION' is set. Unset this variable to execute "
                    "the query directly into a PyArrow table."
                ),
                log_level=logging.DEBUG,
            )

        if finalized_query.finalizer in (Finalizer.FIRST, Finalizer.ONE, Finalizer.ONE_OR_NONE):
            raise UnsupportedEfficientExecutionError(
                (
                    f"Falling back to SQLAlchemy execution for finalizer '{finalized_query.finalizer.value}', "
                    "as it is faster for small results."
                ),
                log_level=logging.DEBUG,
            )

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(
                finalized_query.query, _supported_sqlalchemy_types_for_pa_csv_querying
            )

        assert len(finalized_query.temp_tables) == 0, "Should not create temp tables with postgres source"

        if polars_read_csv:
            try:
                return self._get_parsed_table_via_polars(finalized_query, connection, columns_to_converters)
            except Exception as e:
                _logger.error("Failed to parse CSV with Polars, falling back to PyArrow CSV reader", exc_info=e)

        buffer = self._get_result_csv_buffer(finalized_query, connection=connection, escape_char="\\")

        # Peek the column names
        first_line = buffer.readline()
        column_names = list(
            csv.reader([first_line.decode("utf8")], escapechar="\\", doublequote=False, quoting=csv.QUOTE_ALL)
        )[0]
        buffer.seek(0)
        converters = columns_to_converters(column_names)

        if env_var_bool("CSV_READ_THEN_CAST"):
            # This seems to tolerant unzoned datetimes better
            parsed_table = pyarrow.csv.read_csv(
                buffer,
                parse_options=pyarrow.csv.ParseOptions(
                    newlines_in_values=True,
                    escape_char="\\",
                    double_quote=False,
                ),
                convert_options=pyarrow.csv.ConvertOptions(
                    true_values=["t"],
                    false_values=["f"],
                    strings_can_be_null=True,
                    quoted_strings_can_be_null=False,
                ),
            )

            if len(converters) != len(parsed_table.column_names):
                _logger.warn(
                    f"mismatch in number of columns between query and converters: {len(converters)=}, {len(parsed_table.column_names)=}"
                )

            restricted_schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
            try:
                return parsed_table.cast(restricted_schema)
            except:
                _logger.warn(f"Falling back from cast in postgres")
                return parsed_table.select([c for c in converters.keys()]).cast(restricted_schema)

        else:
            schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
            return pyarrow.csv.read_csv(
                buffer,
                parse_options=pyarrow.csv.ParseOptions(
                    newlines_in_values=True,
                    escape_char="\\",
                    double_quote=False,
                ),
                convert_options=pyarrow.csv.ConvertOptions(
                    true_values=["t"],
                    false_values=["f"],
                    strings_can_be_null=True,
                    quoted_strings_can_be_null=False,
                    column_types=schema,
                ),
            )


def _reformat_compiled_query_string_for_csv_output(
    stmt: str,
    *,
    escape_char: str,
    named_params: Mapping[str, Any],
) -> str:
    """
    - Replaces named parameters like `:foo` with the python3-style `{foo}` which is what `psycopg2.sql.SQL.format`
    expects to see in its inputs.

    - Wraps the provided `stmt` in a `COPY _ to STDOUT` declaration to format it as a CSV.
    """
    # Forcing quote so the unquoted empty string will represent null values

    # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects

    original_stmt = stmt
    import sqlglot
    import sqlglot.expressions

    try:
        stmt_expression = sqlglot.parse_one(stmt, read="postgres")
        for placeholder in list(stmt_expression.find_all(sqlglot.expressions.Placeholder)):
            if isinstance(placeholder.this, str) and placeholder.this in named_params:
                # If this is a known placeholder like `:foo`, replace it verbatim with `{foo}`.
                # The use of the 'var' node here is incidental - it accepts any string as argument,
                # and sqlglot will reproduce that string verbatim as output.
                placeholder.replace(sqlglot.expressions.var("{" + placeholder.this + "}"))
        stmt = stmt_expression.sql(dialect="postgres")

        stmt = f"COPY ({stmt}) TO STDOUT (FORMAT CSV, HEADER true, FORCE_QUOTE *, ESCAPE '{escape_char}')"
    except Exception as e:
        raise ValueError(
            f"Failed to parse and convert postgres output {repr(original_stmt)} with named parameters {repr(list(named_params.keys()))} into valid psycopg2-compatible CSV OUTPUT statement: {e}"
        ) from e

    return stmt


def _get_df_with_parsed_dt_column(pl_table, col_name: str, parser_formats: Sequence[str], target_dtype):
    import polars as pl

    num_nulls_original = pl_table[col_name].null_count()
    original_dt_clone = pl_table[col_name].clone()

    def parsing_complete(table: pl.DataFrame) -> bool:
        if table[col_name].dtype != target_dtype:
            # Never parsed
            return False
        return table[col_name].null_count() == num_nulls_original

    parser_formats = collections.deque(parser_formats)
    # When `fmt=None`, polars will raise a `ComputeError` if it
    # fails parsing, even if `strict=False`. Then, we will fallback
    # to the arrow CSV reader, which will raise a useful error.
    # TODO: Don't depend on pyarrow to raise pyarrow.ArrowInvalid,
    #       instead raise a custom parser error and handle that in
    #       the engine.
    parser_formats.append(None)  # noqa

    # You might think this strptime call can be included in the for
    # loop below, but this is intentionally left out of the for loop
    # because we want to avoid calling `pl.coalesce` for the first pass.
    # Otherwise, the result of the coalescion will be a column of
    # `pl.Utf8` instead of the target date or datetime type.
    pl_table = pl_table.with_columns(
        original_dt_clone.str.strptime(
            target_dtype,
            fmt=parser_formats.popleft(),
            strict=False,
        ).alias(col_name)
    )

    # Incrementally coalesce so that we don't have to do all
    # passes of parsing - only as many as needed.
    while len(parser_formats) > 0 and not parsing_complete(pl_table):
        fmt = parser_formats.popleft()
        formatted_col = original_dt_clone.str.strptime(
            target_dtype,
            fmt=fmt,
            strict=False,
        ).alias(col_name)
        coalesced_col = pl.coalesce(
            pl.col(col_name),
            formatted_col,
        )
        pl_table = pl_table.with_columns(coalesced_col)

    # We would have raised if there was an error parsing with `fmt=None`.
    assert parsing_complete(pl_table)

    return pl_table
