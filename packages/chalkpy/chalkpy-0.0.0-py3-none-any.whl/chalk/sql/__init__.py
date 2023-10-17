from os import PathLike
from typing import Any, Dict, Optional, Union, overload

from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.databricks import DatabricksSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteSourceImpl
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    SQLSourceWithTableIngestProtocol,
    StringChalkQueryProtocol,
    TableIngestProtocol,
)


@overload
def SnowflakeSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Snowflake database.

    If you have only one Snowflake connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource()
    """


@overload
def SnowflakeSource(*, name: str, engine_args: Optional[Dict[str, Any]] = ...) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource(name="RISK")
    """
    ...


@overload
def SnowflakeSource(
    *,
    account_identifier: str = ...,
    warehouse: str = ...,
    user: str = ...,
    password: str = ...,
    db: str = ...,
    schema: str = ...,
    role: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    account_identifier
        Your Snowflake account identifier.
    warehouse
        Snowflake warehouse to use.
    user
        Username to connect to Snowflake.
    password
        The password to use.
    db
        Database to use.
    schema
        Snowflake schema in the database to use.
    role
        Snowflake role name to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> snowflake = SnowflakeSource(
    ...     db=os.getenv("SNOWSQL_DATABASE"),
    ...     schema=os.getenv("SNOWSQL_SCHEMA"),
    ...     role=os.getenv("SNOWSQL_ROLE"),
    ...     warehouse=os.getenv("SNOWSQL_WAREHOUSE"),
    ...     user=os.getenv("SNOWSQL_USER"),
    ...     password=os.getenv("SNOWSQL_PWD"),
    ...     account_identifier=os.getenv("SNOWSQL_ACCOUNT_IDENTIFIER")
    ... )
    """
    ...


def SnowflakeSource(
    *,
    name: Optional[str] = None,
    account_identifier: Optional[str] = None,
    warehouse: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    db: Optional[str] = None,
    schema: Optional[str] = None,
    role: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Snowflake data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return SnowflakeSourceImpl(
        name=name,
        account_identifier=account_identifier,
        warehouse=warehouse,
        user=user,
        password=password,
        db=db,
        schema=schema,
        role=role,
        engine_args=engine_args,
    )


@overload
def PostgreSQLSource() -> SQLSourceWithTableIngestProtocol:
    """Connect to the only configured PostgreSQL database.

    If you have only one PostgreSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> pg = PostgreSQLSource()
    """
    ...


@overload
def PostgreSQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """If you have only one PostgreSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = PostgreSQLSource(name="RISK")
    """
    ...


@overload
def PostgreSQLSource(
    *,
    host: str = ...,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        PostgreSQL username to connect as.
    password
        The password to be used if the server demands password authentication.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> pg = PostgreSQLSource(
    ...     host=os.getenv("PGHOST"),
    ...     port=os.getenv("PGPORT"),
    ...     db=os.getenv("PGDATABASE"),
    ...     user=os.getenv("PGUSER"),
    ...     password=os.getenv("PGPASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return pg.query_string("select name from users where id = 4").one()
    """
    ...


def PostgreSQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> TableIngestProtocol:
    """Create a PostgreSQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return PostgreSQLSourceImpl(
        host, port, db, user, password, name, engine_args=engine_args, async_engine_args=async_engine_args
    )


@overload
def MySQLSource() -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> mysql = MySQLSource()
    """
    ...


@overload
def MySQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = MySQLSource(name="RISK")
    """
    ...


@overload
def MySQLSource(
    *,
    host: str,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """
    You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        MySQL username to connect as.
    password
        The password to be used if the server demands password authentication.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args:
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> mysql = MySQLSource(
    ...     host=os.getenv("PGHOST"),
    ...     port=os.getenv("PGPORT"),
    ...     db=os.getenv("PGDATABASE"),
    ...     user=os.getenv("PGUSER"),
    ...     password=os.getenv("PGPASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return mysql.query_string("select name from users where id = 4").one()
    """
    ...


def MySQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Create a MySQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return MySQLSourceImpl(
        host, port, db, user, password, name, engine_args=engine_args, async_engine_args=async_engine_args
    )


def SQLiteInMemorySource(
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Testing SQL source.

    If you have only one SQLiteInMemorySource integration, there's no need to provide
    a distinguishing name.

    Parameters
    ----------
    name
        The name of the integration.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SQLiteInMemorySource(name="RISK")
    """
    return SQLiteSourceImpl(name=name, engine_args=engine_args, async_engine_args=async_engine_args)


def SQLiteFileSource(
    filename: Union[str, PathLike],
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Create a SQLite source for a file.

    Parameters
    ----------
    filename
        The name of the file.
    name
        The name to use in testing
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.
    """
    return SQLiteSourceImpl(filename=filename, name=name, engine_args=engine_args, async_engine_args=async_engine_args)


@overload
def RedshiftSource() -> BaseSQLSourceProtocol:
    """If you have only one Redshift connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource()
    """
    ...


@overload
def RedshiftSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Redshift integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource(name="RISK")
    """
    ...


@overload
def RedshiftSource(
    *,
    host: str = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    port: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    db
        The database name.
    user
        Redshify username to connect as.
    password
        The password for the Redshift database.
    port
        Port number to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> redshift = RedshiftSource(
    ...     host=os.getenv("REDSHIFT_HOST"),
    ...     db=os.getenv("REDSHIFT_DB"),
    ...     user=os.getenv("REDSHIFT_USER"),
    ...     password=os.getenv("REDSHIFT_PASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return redshift.query_string("select name from users where id = 4").one()
    """
    ...


def RedshiftSource(
    *,
    host: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Redshift data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return RedshiftSourceImpl(host, db, user, password, name, port, engine_args=engine_args)


@overload
def BigQuerySource() -> BaseSQLSourceProtocol:
    """If you have only one BigQuery connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource()
    """
    ...


@overload
def BigQuerySource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one BigQuery integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource(name="RISK")
    """
    ...


@overload
def BigQuerySource(
    *,
    project: Optional[str] = ...,
    dataset: Optional[str] = ...,
    location: Optional[str] = ...,
    credentials_base64: Optional[str] = ...,
    credentials_path: Optional[str] = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    project
        The name of the GCP project for the BigQuery instance.
    dataset
        The name of the BigQuery dataset.
    location
        The location of the BigQuery instance.
    credentials_base64
        The credentials to use to connect, encoded as a base64 string.
    credentials_path
        The path to the credentials file to use to connect.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> source = BigQuerySource(
    ...     project=os.getenv("BIGQUERY_PROJECT"),
    ...     dataset=os.getenv("BIGQUERY_DATASET"),
    ...     location=os.getenv("BIGQUERY_LOCATION"),
    ...     credentials_base64=os.getenv("BIGQUERY_CREDENTIALS_BASE64"),
    ... )
    """
    ...


def BigQuerySource(
    *,
    name: Optional[str] = None,
    project: Optional[str] = None,
    dataset: Optional[str] = None,
    location: Optional[str] = None,
    credentials_base64: Optional[str] = None,
    credentials_path: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a BigQuery data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return BigQuerySourceImpl(
        name=name,
        project=project,
        dataset=dataset,
        location=location,
        credentials_base64=credentials_base64,
        credentials_path=credentials_path,
        engine_args=engine_args,
    )


@overload
def CloudSQLSource() -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource()
    """
    ...


@overload
def CloudSQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource(name="RISK")
    """
    ...


@overload
def CloudSQLSource(
    *,
    instance_name: Optional[str] = ...,
    db: Optional[str] = ...,
    user: Optional[str] = ...,
    password: Optional[str] = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    instance_name
        The name of the Cloud SQL instance, as defined in your GCP console.
    db
        Database to use.
    user
        Username to use.
    password
        The password to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> CloudSQLSource(
    ...     instance_name=os.getenv("CLOUDSQL_INSTANCE_NAME"),
    ...     db=os.getenv("CLOUDSQL_DB"),
    ...     user=os.getenv("CLOUDSQL_USER"),
    ...     password=os.getenv("CLOUDSQL_PASSWORD"),
    ... )
    """


def CloudSQLSource(
    *,
    name: Optional[str] = None,
    instance_name: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a CloudSQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return CloudSQLSourceImpl(
        name=name,
        instance_name=instance_name,
        db=db,
        user=user,
        password=password,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


@overload
def DatabricksSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Databricks database.

    If you have only one Databricks connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DatabricksSource()
    """


@overload
def DatabricksSource(*, name: str, engine_args: Optional[Dict[str, Any]] = ...) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DatabricksSource(name="RISK")
    """
    ...


@overload
def DatabricksSource(
    *,
    host: str = ...,
    http_path: str = ...,
    access_token: str = ...,
    db: str = ...,
    port: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Your Databricks host.
    http_path
        Databricks HTTP path to use.
    access_token
        Access token to connect to Databricks.
    db
        Database to use.
    port
        Port number to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> databricks = DatabricksSource(
    ...     host=os.getenv("DATABRICKS_HOST"),
    ...     http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    ...     access_token=os.getenv("DATABRICKS_TOKEN"),
    ...     db=os.getenv("DATABRICKS_DATABASE"),
    ...     port=os.getenv("DATABRICKS_PORT"),
    ... )
    """
    ...


def DatabricksSource(
    *,
    name: Optional[str] = None,
    host: Optional[str] = None,
    http_path: Optional[str] = None,
    access_token: Optional[str] = None,
    db: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Databricks data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return DatabricksSourceImpl(
        host=host,
        http_path=http_path,
        access_token=access_token,
        db=db,
        port=port,
        name=name,
        engine_args=engine_args,
    )


__all__ = [
    "BaseSQLSourceProtocol",
    "BigQuerySource",
    "CloudSQLSource",
    "DatabricksSource",
    "MySQLSource",
    "PostgreSQLSource",
    "RedshiftSource",
    "SQLiteFileSource",
    "SQLiteInMemorySource",
    "SnowflakeSource",
    "FinalizedChalkQuery",
    "ChalkQueryProtocol",
    "StringChalkQueryProtocol",
    "TableIngestProtocol",
    "SQLSourceWithTableIngestProtocol",
    "IncrementalSettings",
]
