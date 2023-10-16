from __future__ import annotations

import dataclasses
import uuid
from datetime import datetime
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Mapping, Optional, Sequence, Union

import numpy as np
from pydantic import BaseModel, Field, root_validator
from typing_extensions import TypeAlias

from chalk.byte_transmit.model import ByteBaseModel, ByteDict
from chalk.features import Feature, ensure_feature
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features.resolver import Resolver
from chalk.features.tag import EnvironmentId
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


def _category_for_error_code(c: Union[ErrorCode, str]) -> ErrorCodeCategory:
    c = ErrorCode[c]
    return {
        ErrorCode.PARSE_FAILED: ErrorCodeCategory.REQUEST,
        ErrorCode.RESOLVER_NOT_FOUND: ErrorCodeCategory.REQUEST,
        ErrorCode.INVALID_QUERY: ErrorCodeCategory.REQUEST,
        ErrorCode.VALIDATION_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.RESOLVER_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.RESOLVER_TIMED_OUT: ErrorCodeCategory.FIELD,
        ErrorCode.UPSTREAM_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.UNAUTHENTICATED: ErrorCodeCategory.NETWORK,
        ErrorCode.UNAUTHORIZED: ErrorCodeCategory.NETWORK,
        ErrorCode.INTERNAL_SERVER_ERROR: ErrorCodeCategory.NETWORK,
        ErrorCode.CANCELLED: ErrorCodeCategory.NETWORK,
        ErrorCode.DEADLINE_EXCEEDED: ErrorCodeCategory.NETWORK,
    }[c]


class OnlineQueryContext(BaseModel):
    """Context in which to execute a query."""

    environment: Optional[str] = None
    """
    The environment under which to run the resolvers.
    API tokens can be scoped to an # environment.
    If no environment is specified in the query,
    but the token supports only a single environment,
    then that environment will be taken as the scope
    for executing the request.
    """

    tags: Optional[List[str]] = None
    """
    The tags used to scope the resolvers.
    More information at https://docs.chalk.ai/docs/resolver-tags
    """


class OfflineQueryContext(BaseModel):
    environment: Optional[str] = None
    """
    The environment under which to run the resolvers.
    API tokens can be scoped to an # environment.
    If no environment is specified in the query,
    but the token supports only a single environment,
    then that environment will be taken as the scope
    for executing the request.
    """


class ErrorCode(str, Enum):
    """The detailed error code.

    For a simpler category of error, see `ErrorCodeCategory`.
    """

    PARSE_FAILED = "PARSE_FAILED"
    """The query contained features that do not exist."""

    RESOLVER_NOT_FOUND = "RESOLVER_NOT_FOUND"
    """
    A resolver was required as part of running the dependency
    graph that could not be found.
    """

    INVALID_QUERY = "INVALID_QUERY"
    """
    The query is invalid. All supplied features need to be
    rooted in the same top-level entity.
    """

    VALIDATION_FAILED = "VALIDATION_FAILED"
    """
    A feature value did not match the expected schema
    (e.g. `incompatible type "int"; expected "str"`)
    """

    RESOLVER_FAILED = "RESOLVER_FAILED"
    """The resolver for a feature errored."""

    RESOLVER_TIMED_OUT = "RESOLVER_TIMED_OUT"
    """The resolver for a feature timed out."""

    UPSTREAM_FAILED = "UPSTREAM_FAILED"
    """
    A crash in a resolver that was to produce an input for
    the resolver crashed, and so the resolver could not run
    crashed, and so the resolver could not run.
    """

    UNAUTHENTICATED = "UNAUTHENTICATED"
    """The request was submitted with an invalid authentication header."""

    UNAUTHORIZED = "UNAUTHORIZED"
    """The supplied credentials do not provide the right authorization to execute the request."""

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    """An unspecified error occurred."""

    CANCELLED = "CANCELLED"
    """The operation was cancelled, typically by the caller."""

    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    """The deadline expired before the operation could complete."""


class ErrorCodeCategory(str, Enum):
    """The category of an error.

    For more detailed error information, see `ErrorCode`
    """

    REQUEST = "REQUEST"
    """
    Request errors are raised before execution of your
    resolver code. They may occur due to invalid feature
    names in the input or a request that cannot be satisfied
    by the resolvers you have defined.
    """

    FIELD = "FIELD"
    """
    Field errors are raised while running a feature resolver
    for a particular field. For this type of error, you'll
    find a feature and resolver attribute in the error type.
    When a feature resolver crashes, you will receive null
    value in the response. To differentiate from a resolver
    returning a null value and a failure in the resolver,
    you need to check the error schema.
    """

    NETWORK = "NETWORK"
    """
    Network errors are thrown outside your resolvers.
    For example, your request was unauthenticated,
    connection failed, or an error occurred within Chalk.
    """


class ChalkException(BaseModel, frozen=True):
    """Information about an exception from a resolver run."""

    kind: str
    """The name of the class of the exception."""

    message: str
    """The message taken from the exception."""

    stacktrace: str
    """The stacktrace produced by the code."""

    internal_stacktrace: Optional[str] = None
    """The stacktrace produced by the code, full detail."""


class ChalkError(BaseModel, frozen=True):
    """
    The `ChalkError` describes an error from running a resolver
    or from a feature that can't be validated.
    """

    code: ErrorCode
    """The type of the error."""

    category: ErrorCodeCategory = ErrorCodeCategory.NETWORK
    """
    The category of the error, given in the type field for the error codes.
    This will be one of "REQUEST", "NETWORK", and "FIELD".
    """

    message: str
    """A readable description of the error message."""

    display_primary_key: Optional[str] = None
    """
    A human-readable hint that can be used to identify the entity that this error is associated with.
    """

    display_primary_key_fqn: Optional[str] = None
    """
    If provided, can be used to add additional context to 'display_primary_key'.
    """

    exception: Optional[ChalkException] = None
    """The exception that caused the failure, if applicable."""

    feature: Optional[str] = None
    """
    The fully qualified name of the failing feature, e.g. `user.identity.has_voip_phone`.
    """

    resolver: Optional[str] = None
    """
    The fully qualified name of the failing resolver, e.g. `my.project.get_fraud_score`.
    """

    def copy_for_feature(self, feature: str) -> "ChalkError":
        return self.copy(update={"feature": feature})

    def copy_for_pkey(self, pkey: Union[str, int]) -> "ChalkError":
        return self.copy(update={"display_primary_key": str(pkey)})

    @root_validator
    def _validate_category(cls, values: Dict[str, Any]):
        values["category"] = _category_for_error_code(values["code"])
        return values

    if TYPE_CHECKING:
        # Defining __hash__ only when type checking
        # since pydantic provides a hash for frozen models
        def __hash__(self) -> int:  # type: ignore
            ...


class ResolverRunStatus(str, Enum):
    """Status of a scheduled resolver run."""

    RECEIVED = "received"
    """The request to run the resolver has been received, and is running or scheduled."""

    SUCCEEDED = "succeeded"
    """The resolver run failed."""

    FAILED = "failed"
    """The resolver run succeeded."""


class ResolverRunResponse(BaseModel):
    """Status of a scheduled resolver run."""

    id: str
    """The ID of the resolver run."""

    status: ResolverRunStatus
    """The current status of the resolver run."""


class WhoAmIResponse(BaseModel):
    """Response for checking the authenticated user."""

    user: str
    """The ID of the user or service token making the query."""


class FeatureResolutionMeta(BaseModel, frozen=True):
    """Detailed metadata about the execution of an online query."""

    chosen_resolver_fqn: str
    """The name of the resolver that computed the feature value."""

    cache_hit: bool
    """Whether the feature request was satisfied by a cached value."""

    primitive_type: Optional[str] = None
    """
    Primitive type name for the feature, e.g. `str` for `some_feature: str`.
    Returned only if query-level 'include_meta' is True.
    """

    version: int = 1
    """
    The version that was selected for this feature. Defaults to `default_version`, if query
    does not specify a constraint. If no versioning information is provided on the feature definition,
    the default version is `1`.
    """


class FeatureResult(BaseModel):
    field: str
    """
    The name of the feature requested, e.g. 'user.identity.has_voip_phone'.
    """

    value: Any  # Value should be a TJSON type
    """
    The value of the requested feature.
    If an error was encountered in resolving this feature,
    this field will be empty.
    """

    pkey: Any = None
    """The primary key of the resolved feature."""

    error: Optional[ChalkError] = None
    """
    The error code encountered in resolving this feature.
    If no error occurred, this field is empty.
    """

    ts: Optional[datetime] = None
    """
    The time at which this feature was computed.
    This value could be significantly in the past if you're using caching.
    """

    meta: Optional[FeatureResolutionMeta] = None
    """Detailed information about how this feature was computed."""


class ExchangeCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str


class ExchangeCredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    # expires_at: datetime
    api_server: str
    primary_environment: Optional[str] = None
    engines: Optional[Mapping[str, str]] = None


class OfflineQueryInput(BaseModel):
    columns: List[str]
    values: List[List[Any]]  # Values should be of type TJSON


class OnlineQueryRequest(BaseModel):
    inputs: Mapping[str, Any]  # Values should be of type TJSON
    outputs: List[str]
    now: Optional[str] = None  # iso format so we can json
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext] = None
    include_meta: bool = True
    explain: Union[bool, Literal["only"]] = False
    skip_online_storage: Optional[bool] = False
    skip_offline_storage: Optional[bool] = False
    skip_metrics_storage: Optional[bool] = False
    skip_cache_lookups: Optional[bool] = False
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    deployment_id: Optional[str] = None
    branch_id: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None
    store_plan_stages: Optional[bool] = False
    gcs_client: Optional[Any] = None
    encoding_options: FeatureEncodingOptions = FeatureEncodingOptions()


@dataclasses.dataclass
class OnlineQuery:
    input: Union[Mapping[FeatureReference, Sequence[Any]], Any]
    output: List[str]
    staleness: Optional[Mapping[str, str]] = None
    tags: Optional[List[str]] = None


class OnlineQueryManyRequest(BaseModel):
    inputs: Mapping[str, List[Any]]
    outputs: List[str]
    now: Optional[List[str]] = None
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext] = None
    include_meta: bool = True
    explain: bool = False
    skip_online_storage: Optional[bool] = False
    skip_offline_storage: Optional[bool] = False
    skip_metrics_storage: Optional[bool] = False
    skip_cache_lookups: Optional[bool] = False
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    deployment_id: Optional[str] = None
    branch_id: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None
    store_plan_stages: Optional[bool] = False
    gcs_client: Optional[Any] = None  # deprecated
    encoding_options: FeatureEncodingOptions = FeatureEncodingOptions()


class TriggerResolverRunRequest(BaseModel):
    resolver_fqn: str


class QueryMeta(BaseModel):
    execution_duration_s: float
    """
    The time, expressed in seconds, that Chalk spent executing this query.
    """

    deployment_id: Optional[str] = None
    """
    The id of the deployment that served this query.
    """

    environment_id: Optional[str] = None
    """
    The id of the environment that served this query. Not intended to be human readable, but helpful for support.
    """

    environment_name: Optional[str] = None
    """
    The short name of the environment that served this query. For example: "dev" or "prod".
    """

    query_id: Optional[str] = None
    """
    A unique ID generated and persisted by Chalk for this query. All computed features, metrics, and logs are
    associated with this ID. Your system can store this ID for audit and debugging workflows.
    """

    query_timestamp: Optional[datetime] = None
    """
    At the start of query execution, Chalk computes 'datetime.now()'. This value is used to timestamp computed features.
    """

    query_hash: Optional[str] = None
    """
    Deterministic hash of the 'structure' of the query. Queries that have the same input/output features will
    typically have the same hash; changes may be observed over time as we adjust implementation details.
    """

    explain_output: Optional[str] = None
    """
    An unstructured string containing diagnostic information about the query execution. Only included if `explain` is True.
    """


class OnlineQueryResponse(BaseModel):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]] = None
    meta: Optional[QueryMeta] = None

    def for_fqn(self, fqn: str):
        return next((x for x in self.data if x.field == fqn), None)

    class Config:
        json_encoders = {
            np.integer: int,
            np.floating: float,
        }


@dataclasses.dataclass
class BulkOnlineQueryResult:
    """
    Represents the result of a single `OnlineQuery`, returned by
    `query_bulk`.

    The `scalars_df` member holds the primary results of the `OnlineQuery`.
    Access this data using `to_polars()` or `to_pandas()`.
    """

    scalars_df: Optional[pl.DataFrame]
    groups_dfs: Optional[Dict[str, pl.DataFrame]]  # change to chalk df whenever we figure out pydantic
    errors: Optional[List[ChalkError]]
    meta: Optional[QueryMeta]

    def to_polars(self) -> pl.DataFrame:
        """
        Allows access to the results of an `OnlineQuery` submitted to `query_bulk` as a Polars dataframe.
        """

        return self.scalars_df or pl.DataFrame()

    def to_pandas(self) -> pd.DataFrame:
        """
        Allows access to the results of an `OnlineQuery` submitted to `query_bulk` as a Pandas dataframe.
        """

        if self.scalars_df is not None:
            return self.scalars_df.to_pandas()
        else:
            return pl.DataFrame().to_pandas()

    # def get_feature_value(self, pkey: str | int, f: FeatureReference):
    #     f_casted = ensure_feature(f)
    #     if f_casted.is_has_many:
    #         return self.groups_dfs[f_casted.root_fqn]
    #     else:
    #         return self.scalars_df[0][f_casted.root_fqn].item()


@dataclasses.dataclass
class BulkOnlineQueryResponse:
    results: List[BulkOnlineQueryResult]

    def __getitem__(self, item: int):
        """
        Support `client.query_bulk(...)[0]` syntax.
        """

        if isinstance(item, int):
            return self.results[item]


FeatureReference: TypeAlias = Union[str, Any]


class CreateOfflineQueryJobRequest(BaseModel):
    output: List[str] = Field(description="A list of output feature root fqns to query")
    required_output: List[str] = Field(default_factory=list, description="A list of required output feature root fqns")
    destination_format: str = Field(description="The desired output format. Should be 'CSV' or 'PARQUET'")
    job_id: Optional[uuid.UUID] = Field(
        default=None,
        description=(
            "A unique job id. If not specified, one will be auto generated by the server. If specified by the client, "
            "then jobs with the same ID will be rejected."
        ),
    )
    input: Optional[OfflineQueryInput] = Field(default=None, description="Any givens")
    max_samples: Optional[int] = Field(
        default=None,
        description="The maximum number of samples. If None, no limit",
    )
    max_cache_age_secs: Optional[int] = Field(
        default=None,  # Defaults to ``OFFLINE_QUERY_MAX_CACHE_AGE_SECS`` in the chalkengine config
        description=(
            "The maximum staleness, in seconds, for how old the view on the offline store can be. That is, "
            "data ingested within this interval will not be reflected in this offline query. "
            "Set to ``0`` to ignore the cache. If not specified, it defaults to 30 minutes."
        ),
    )
    observed_at_lower_bound: Optional[str] = Field(
        default=None,
        description="The lower bound for the observed at timestamp (inclusive). If not specified, defaults to the beginning of time",
    )
    observed_at_upper_bound: Optional[str] = Field(
        default=None,
        description="The upper bound for the observed at timestamp (inclusive). If not specified, defaults to the end of time.",
    )
    dataset_name: Optional[str] = None
    branch: Optional[str] = None
    recompute_features: Union[bool, List[FeatureReference]] = False
    store_plan_stages: bool = False
    explain: Union[bool, Literal["onlyu"]] = False
    tags: Optional[List[str]] = None
    correlation_id: Optional[str] = None


class ComputeResolverOutputRequest(BaseModel):
    input: OfflineQueryInput
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class DatasetRecomputeRequest(BaseModel):
    dataset_name: Optional[str] = None
    branch: str
    dataset_id: Optional[str] = None
    revision_id: Optional[str] = None
    features: List[str]


class RecomputeResolverOutputRequest(BaseModel):
    persistent_id: str
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class ComputeResolverOutputResponse(BaseModel):
    job_id: str
    persistent_id: str
    errors: Optional[List[ChalkError]] = None


class OfflineQueryRequest(BaseModel):
    """V1 OfflineQueryRequest. Not used by the current Chalk Client."""

    output: List[str]  # output features which can be null
    input: Optional[OfflineQueryInput] = None
    dataset: Optional[str] = None
    max_samples: Optional[int] = None
    max_cache_age_secs: Optional[int] = None
    required_outputs: List[str] = Field(default_factory=list)  # output features which cannot be null


class OfflineQueryResponse(BaseModel):
    """V1 OfflineQueryResponse. Not used by the current Chalk Client."""

    columns: List[str]
    output: List[List[Any]]  # values should be of TJSON types
    errors: Optional[List[ChalkError]] = None


class CreateOfflineQueryJobResponse(BaseModel):
    """
    Attributes:
        job_id: A job ID, which can be used to retrieve the results.
    """

    job_id: uuid.UUID
    version: int = 1  # Field is deprecated
    errors: Optional[List[ChalkError]] = None


class ColumnMetadata(BaseModel):
    feature_fqn: str = Field(description="The root FQN of the feature for a column")

    column_name: str = Field(description="The name of the column that corresponds to this feature")

    dtype: str = Field(description="The data type for this feature")
    # This field is currently a JSON-stringified version of the SerializeDType property
    # Using a string instead of a pydantic model the SerializedDType encoding does not affect
    # the api layer


class GetOfflineQueryJobResponse(BaseModel):
    is_finished: bool = Field(description="Whether the export job is finished (it runs asynchronously)")
    version: int = Field(
        default=1,  # Backwards compatibility
        description=(
            "Version number representing the format of the data. The client uses this version number "
            "to properly decode and load the query results into DataFrames."
        ),
    )
    urls: List[str] = Field(
        description="A list of short-lived, authenticated URLs that the client can download to retrieve the exported data."
    )
    errors: Optional[List[ChalkError]] = None
    columns: Optional[List[ColumnMetadata]] = Field(
        description="Expected columns for the dataframe, including data type information",
        default=None,
    )


class QueryStatus(IntEnum):
    PENDING_SUBMISSION = 1
    """Pending submission to the database."""
    SUBMITTED = 2
    """Submitted to the database, but not yet running."""
    RUNNING = 3
    """Running in the database."""
    ERROR = 4
    """Error with either submitting or running the job."""
    EXPIRED = 5
    """The job did not complete before an expiration deadline, so there are no results."""
    CANCELLED = 6
    """Manually cancelled before it errored or finished successfully."""
    SUCCESSFUL = 7  #
    """Successfully ran the job."""


class DatasetSampleFilter(BaseModel):
    lower_bound: Optional[datetime] = None
    upper_bound: Optional[datetime] = None
    max_samples: Optional[int] = None


class DatasetFilter(BaseModel):
    sample_filters: DatasetSampleFilter = Field(default_factory=DatasetSampleFilter)
    max_cache_age_secs: Optional[float] = None


class DatasetRevisionResponse(BaseModel):
    dataset_name: Optional[str] = None
    dataset_id: Optional[uuid.UUID] = None
    environment_id: EnvironmentId
    revision_id: Optional[uuid.UUID] = None  # Currently, the revision ID is the job ID that created the revision
    creator_id: str
    outputs: List[str]
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None
    givens_uri: Optional[str] = None
    status: QueryStatus
    filters: DatasetFilter
    num_partitions: int
    num_bytes: Optional[int] = None
    output_uris: str
    output_version: int
    branch: Optional[str] = None


class DatasetRecomputeResponse(DatasetRevisionResponse):
    errors: Optional[List[ChalkError]] = None

    @classmethod
    def from_revision_response(
        cls, revision: DatasetRevisionResponse, errors: Optional[List[ChalkError]] = None
    ) -> "DatasetRecomputeResponse":
        return cls(
            revision_id=revision.revision_id,
            environment=revision.environment_id,
            creator_id=revision.creator_id,
            outputs=revision.outputs,
            givens_uri=revision.givens_uri,
            status=revision.status,
            filters=revision.filters,
            num_partitions=revision.num_partitions,
            output_uris=revision.output_uris,
            output_version=revision.output_version,
            num_bytes=revision.num_bytes,
            created_at=revision.created_at,
            started_at=revision.started_at,
            terminated_at=revision.terminated_at,
            dataset_name=revision.dataset_name,
            dataset_id=revision.dataset_id,
            branch=revision.branch,
            errors=errors,
        )


class DatasetResponse(BaseModel):
    is_finished: bool = Field(description="Whether the export job is finished (it runs asynchronously)")
    version: int = Field(
        default=1,  # Backwards compatibility
        description=(
            "Version number representing the format of the data. The client uses this version number "
            "to properly decode and load the query results into DataFrames."
        ),
    )
    environment_id: EnvironmentId
    dataset_id: Optional[uuid.UUID] = None
    dataset_name: Optional[str] = None
    revisions: List[DatasetRevisionResponse]
    errors: Optional[List[ChalkError]] = None


class SingleEntityUpdate(BaseModel):
    entity_type: Literal["feature", "resolver"]
    entity_fqn: str
    entity_shortname: str

    @classmethod
    def for_resolver(cls, resolver: Resolver) -> "SingleEntityUpdate":
        return cls(
            entity_type="resolver",
            entity_fqn=resolver.fqn,
            entity_shortname=resolver.fqn.split(".")[-1],
        )

    @classmethod
    def for_feature(cls, feature: Feature) -> "SingleEntityUpdate":
        return cls(
            entity_type="feature",
            entity_fqn=feature.fqn,
            entity_shortname=feature.name,
        )


class UpdateGraphEntityResponse(BaseModel):
    """
    Represents the result of live updating a graph entity like a resolver or feature class.
    This may result in multiple individual resolvers/features being updated, e.g. if the user
    adds a new feature class w/ multiple new fields.
    """

    added: Optional[List[SingleEntityUpdate]] = None
    modified: Optional[List[SingleEntityUpdate]] = None
    removed: Optional[List[SingleEntityUpdate]] = None

    errors: Optional[List[ChalkError]] = None


class UpdateResolverResponse(BaseModel):
    updated_fqn: Optional[
        str
    ] = None  # The resolver fqn that was updated (may not be the same as the one that was requested)
    is_new: Optional[bool] = None  # Whether a new resolver was created, or if an existing one was replaced
    errors: Optional[List[ChalkError]] = None


class FeatureObservationDeletionRequest(BaseModel):
    """
    Represents a request to target particular feature observations for deletion. Note that
    the "features" and "tags" fields are mutually exclusive -- either only one of them is
    specified, or neither is specified, in which case deletion will proceed for all
    features of the primary keys specified.
    """

    namespace: str
    """
    The namespace in which the features targeted for deletion reside.
    """

    features: Optional[List[str]]
    """
    An optional list of the feature names of the features that should be deleted
    for the targeted primary keys. Not specifying this and not specifying the "tags" field
    will result in all features being targeted for deletion for the specified primary keys.
    Note that this parameter and the "tags" parameter are mutually exclusive.
    """

    tags: Optional[List[str]]
    """
    An optional list of tags that specify features that should be targeted for deletion.
    If a feature has a tag in this list, its observations for the primary keys you listed
    will be targeted for deletion. Not specifying this and not specifying the "features"
    field will result in all features being targeted for deletion for the specified primary
    keys. Note that this parameter and the "features" parameter are mutually exclusive.
    """

    primary_keys: List[str]
    """
    The primary keys of the observations that should be targeted for deletion.
    """


class FeatureObservationDeletionResponse(BaseModel):
    """
    Contains ChalkErrors for any failures, if any, that might have occurred when trying
    to delete the features that were requested.
    """

    errors: Optional[List[ChalkError]]


class FeatureDropRequest(BaseModel):
    namespace: str
    """Namespace in which the features targeted for drop reside."""

    features: List[str]
    """Names of the features that should be dropped."""


class FeatureDropResponse(BaseModel):
    """
    Contains ChalkErrors for any failures, if any, that might have occurred when trying
    to drop the features that were requested.
    """

    errors: Optional[List[ChalkError]]


class GetIncrementalProgressResponse(BaseModel):
    """
    Returns information about the current state of an incremental resolver.
    Specifically, the recorded timestamps that the resolver uses to process recent data.
    If both timestamp fields are returned as None, this means the current resolver hasn't
    run yet or hasn't stored any progress data. The next time it runs it will ingest all historical data

    More information at https://docs.chalk.ai/docs/sql#incremental-queries
    """

    environment_id: EnvironmentId

    resolver_fqn: str
    """
    The fully qualified name of the given resolver
    """

    max_ingested_timestamp: Optional[datetime]
    """
    The latest timestamp found in ingested data.
    """

    last_execution_timestamp: Optional[datetime]
    """
    The latest timestamp at which the resolver was run. If configured to do so, the
    resolver uses this timestamp instead of max_ingested_timestamp to filter input data.
    If None, this means that this value isn't currently used by this resolver.
    """

    errors: Optional[List[ChalkError]] = None


class SetIncrementalProgressRequest(BaseModel):
    """
    Sets the current state of an incremental resolver, specifically the timestamps it uses
    to filter inputs to only recent data, to the given timestamps.

    More information at https://docs.chalk.ai/docs/sql#incremental-queries
    """

    max_ingested_timestamp: Optional[datetime] = None
    """
    The latest timestamp found in ingested data.
    Timestamp must have a timezone specified.
    """

    last_execution_timestamp: Optional[datetime] = None
    """
    The latest time the resolver was run. If configured to do so, the
    resolver uses this timestamp instead of max_ingested_timestamp to filter input data.
    Timestamp must have a timezone specified.
    """


class BranchDeployRequest(BaseModel):
    branch_name: str
    """
    Name of the branch. If branch does not exist, it will be created.
    """

    create_only: bool = False
    """
    If true, tries to create a new branch returns an error if the branch already exists.
    """

    source_deployment_id: Optional[str] = None
    """
    Use the given deployment's source on the branch. If None, the latest active deployment will be used.
    """


class BranchDeployResponse(BaseModel):
    branch_name: str
    new_branch_created: bool

    source_deployment_id: str
    branch_deployment_id: str


BranchIdParam: TypeAlias = Union[None, str, type(Ellipsis)]
"""
Type used for the 'branch' paremeter in calls to the Chalk Client.
The branch can either be:
 1. A string that is used as the branch name for the request
 2. None, in which case the request is _not_ sent to a branch server,
 3. Ellipsis (...), indicating that the branch name (or lack thereof) is
    inferred from the ChalkClient's current branch.
"""


class StreamResolverTestStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class StreamResolverTestMessagePayload(BaseModel):
    key: str
    message_str: Optional[str]
    message_bytes: Optional[str]
    timestamp: Optional[datetime]


class StreamResolverTestRequest(BaseModel):
    resolver_fqn: str
    num_messages: Optional[int] = None
    test_messages: Optional[List[StreamResolverTestMessagePayload]] = None


class StreamResolverTestResponse(BaseModel):
    status: StreamResolverTestStatus
    data_uri: Optional[str] = None
    errors: Optional[List[ChalkError]] = None
    message: Optional[str] = None

    @property
    def features(self) -> pl.DataFrame:
        if self.data_uri is None:
            raise ValueError(
                "Features were not saved to storage. "
                "Please inspect 'ResolverTestResponse.errors' and 'ResolverTestResponse.message'."
            )
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        return pl.read_parquet(self.data_uri)


class OnlineQueryResultFeather(ByteBaseModel):
    has_data: bool
    scalar_data: bytes
    groups_data: ByteDict
    errors: Optional[List[str]]  # inner str is json of ChalkError to mimic Optional[List[ChalkError]]
    meta: Optional[str]  # inner str is json of QueryMeta to mimic Optional[QueryMeta]


class OnlineQueryResponseFeather(ByteBaseModel):
    query_results_bytes: ByteDict
