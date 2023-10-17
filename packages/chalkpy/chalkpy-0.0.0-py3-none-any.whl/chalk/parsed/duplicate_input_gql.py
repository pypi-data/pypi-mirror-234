from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureIdGQL:
    fqn: str
    name: str
    namespace: str
    isPrimary: bool
    className: Optional[str] = None
    attributeName: Optional[str] = None
    explicitNamespace: Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertReferencePathComponentGQL:
    parent: UpsertFeatureIdGQL
    child: UpsertFeatureIdGQL
    parentToChildAttributeName: str


@dataclasses_json.dataclass_json
@dataclass
class UpsertFilterGQL:
    lhs: UpsertFeatureIdGQL
    op: str
    rhs: UpsertFeatureIdGQL


@dataclasses_json.dataclass_json
@dataclass
class UpsertDataFrameGQL:
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureReferenceGQL:
    underlying: UpsertFeatureIdGQL
    path: Optional[List[UpsertReferencePathComponentGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasOneKindGQL:
    join: UpsertFilterGQL


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasManyKindGQL:
    join: UpsertFilterGQL
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class VersionInfoGQL:
    version: int
    maximum: int
    default: int
    versions: List[str]


@dataclasses_json.dataclass_json
@dataclass
class UpsertScalarKindGQL:
    primary: bool
    dtype: Optional[str] = None  # The JSON-serialized form of the chalk.features.SerializedDType model
    version: Optional[int] = None  # Deprecated. Use the `versionInfo` instead
    versionInfo: Optional[VersionInfoGQL] = None
    baseClasses: Optional[List[str]] = None  # Deprecated. Use the `dtype` instead
    hasEncoderAndDecoder: bool = False  # Deprecated. Use the `dtype` instead
    scalarKind: Optional[str] = None  # Deprecated. Use the `dtype` instead


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureTimeKindGQL:
    format: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureGQL:
    id: UpsertFeatureIdGQL

    scalarKind: Optional[UpsertScalarKindGQL] = None
    hasManyKind: Optional[UpsertHasManyKindGQL] = None
    hasOneKind: Optional[UpsertHasOneKindGQL] = None
    featureTimeKind: Optional[UpsertFeatureTimeKindGQL] = None
    etlOfflineToOnline: bool = False
    windowBuckets: Optional[List[float]] = None

    tags: Optional[List[str]] = None
    maxStaleness: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None

    namespacePath: Optional[str] = None
    isSingleton: Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclass
class KafkaConsumerConfigGQL:
    broker: List[str]
    topic: List[str]
    sslKeystoreLocation: Optional[str]
    clientIdPrefix: Optional[str]
    groupIdPrefix: Optional[str]
    topicMetadataRefreshIntervalMs: Optional[int]
    securityProtocol: Optional[str]


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamMessageGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamKeyedStateGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None
    defaultValue: Optional[Any] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamGQL:
    message: Optional[UpsertStreamResolverParamMessageGQL]
    state: Optional[UpsertStreamResolverParamKeyedStateGQL]


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    sourceClassName: Optional[str] = None
    sourceConfig: Optional[Any] = None
    machineType: Optional[str] = None
    environment: Optional[List[str]] = None
    output: Optional[List[UpsertFeatureIdGQL]] = None
    inputs: Optional[Sequence[UpsertStreamResolverParamGQL]] = None
    doc: Optional[str] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverOutputGQL:
    features: Optional[List[UpsertFeatureIdGQL]] = None
    dataframes: Optional[List[UpsertDataFrameGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverInputUnionGQL:
    feature: Optional[UpsertFeatureReferenceGQL] = None
    dataframe: Optional[UpsertDataFrameGQL] = None
    pseudoFeature: Optional[UpsertFeatureReferenceGQL] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    output: UpsertResolverOutputGQL
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    cron: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    allInputs: Optional[List[UpsertResolverInputUnionGQL]] = None
    machineType: Optional[str] = None
    owner: Optional[str] = None
    timeout: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertSinkResolverGQL:
    fqn: str
    functionDefinition: str
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machineType: Optional[str] = None
    bufferSize: Optional[int] = None
    debounce: Optional[str] = None
    maxDelay: Optional[str] = None
    upsert: Optional[bool] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None


@dataclasses_json.dataclass_json
@dataclass
class MetadataSettings:
    name: str
    missing: str


@dataclasses_json.dataclass_json
@dataclass
class FeatureSettings:
    metadata: Optional[List[MetadataSettings]] = None


@dataclasses_json.dataclass_json
@dataclass
class ResolverSettings:
    metadata: Optional[List[MetadataSettings]] = None


@dataclasses_json.dataclass_json
@dataclass
class ValidationSettings:
    feature: Optional[FeatureSettings] = None
    resolver: Optional[ResolverSettings] = None


@dataclasses_json.dataclass_json
@dataclass
class EnvironmentSettingsGQL:
    id: str
    runtime: Optional[str]
    requirements: Optional[str]
    dockerfile: Optional[str]
    requiresPackages: Optional[List[str]] = None


@dataclasses_json.dataclass_json
@dataclass
class ProjectSettingsGQL:
    project: str
    environments: Optional[List[EnvironmentSettingsGQL]]
    validation: Optional[ValidationSettings] = None


@dataclasses_json.dataclass_json
@dataclass
class FailedImport:
    filename: str
    module: str
    traceback: str


@dataclasses_json.dataclass_json
@dataclass
class ChalkPYInfo:
    version: str


class MetricKindGQL(str, Enum):
    FEATURE_REQUEST_COUNT = "FEATURE_REQUEST_COUNT"
    FEATURE_LATENCY = "FEATURE_LATENCY"
    FEATURE_STALENESS = "FEATURE_STALENESS"
    FEATURE_VALUE = "FEATURE_VALUE"
    FEATURE_WRITE = "FEATURE_WRITE"
    FEATURE_NULL_RATIO = "FEATURE_NULL_RATIO"

    RESOLVER_REQUEST_COUNT = "RESOLVER_REQUEST_COUNT"
    RESOLVER_LATENCY = "RESOLVER_LATENCY"
    RESOLVER_SUCCESS_RATIO = "RESOLVER_SUCCESS_RATIO"

    QUERY_COUNT = "QUERY_COUNT"
    QUERY_LATENCY = "QUERY_LATENCY"
    QUERY_SUCCESS_RATIO = "QUERY_SUCCESS_RATIO"

    BILLING_INFERENCE = "BILLING_INFERENCE"
    BILLING_CRON = "BILLING_CRON"
    BILLING_MIGRATION = "BILLING_MIGRATION"

    CRON_COUNT = "CRON_COUNT"
    CRON_LATENCY = "CRON_LATENCY"

    STREAM_MESSAGES_PROCESSED = "STREAM_MESSAGES_PROCESSED"
    STREAM_MESSAGE_LATENCY = "STREAM_MESSAGE_LATENCY"

    STREAM_WINDOWS_PROCESSED = "STREAM_WINDOWS_PROCESSED"
    STREAM_WINDOW_LATENCY = "STREAM_WINDOW_LATENCY"


class FilterKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    FEATURE_TAG = "FEATURE_TAG"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"
    RESOLVER_TAG = "RESOLVER_TAG"

    CRON_STATUS = "CRON_STATUS"
    MIGRATION_STATUS = "MIGRATION_STATUS"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"
    OPERATION_ID = "OPERATION_ID"

    QUERY_NAME = "QUERY_NAME"
    QUERY_STATUS = "QUERY_STATUS"

    IS_NULL = "IS_NULL"


class ComparatorKindGQL(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    ONE_OF = "ONE_OF"


class WindowFunctionKindGQL(str, Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"

    PERCENTILE_99 = "PERCENTILE_99"
    PERCENTILE_95 = "PERCENTILE_95"
    PERCENTILE_75 = "PERCENTILE_75"
    PERCENTILE_50 = "PERCENTILE_50"
    PERCENTILE_25 = "PERCENTILE_25"
    PERCENTILE_5 = "PERCENTILE_5"

    ALL_PERCENTILES = "ALL_PERCENTILES"


class GroupByKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    IS_NULL = "IS_NULL"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"

    QUERY_STATUS = "QUERY_STATUS"
    QUERY_NAME = "QUERY_NAME"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"


class MetricFormulaKindGQL(str, Enum):
    SUM = "SUM"
    TOTAL_RATIO = "TOTAL_RATIO"
    RATIO = "RATIO"
    PRODUCT = "PRODUCT"
    ABS = "ABS"
    KS_STAT = "KS_STAT"
    KS_TEST = "KS_TEST"
    KS_THRESHOLD = "KS_THRESHOLD"
    TIME_OFFSET = "TIME_OFFSET"


class AlertSeverityKindGQL(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"


class ThresholdKindGQL(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFilterGQL:
    kind: FilterKindGQL
    comparator: ComparatorKindGQL
    value: List[str]


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigSeriesGQL:
    metric: MetricKindGQL
    filters: List[CreateMetricFilterGQL]
    name: Optional[str] = None
    windowFunction: Optional[WindowFunctionKindGQL] = None
    groupBy: Optional[List[GroupByKindGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateDatasetFeatureOperandGQL:
    """
    Can't do a Tuple[int, str] so we're going to use a wrapper
    """

    dataset: str
    feature: str


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFormulaGQL:
    """
    No input unions in graphql means we have to use parallel optional input keys
    and do additional validation work ourselves
    """

    kind: MetricFormulaKindGQL
    # ----- Input Union ------
    singleSeriesOperands: Optional[int]  # index of a single series
    multiSeriesOperands: Optional[List[int]]  # index of multiple series
    datasetFeatureOperands: Optional[CreateDatasetFeatureOperandGQL]  # dataset id and feature name
    # ----- End Union  ------
    name: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateAlertTriggerGQL:
    name: str
    severity: AlertSeverityKindGQL
    thresholdPosition: ThresholdKindGQL
    thresholdValue: float
    seriesName: Optional[str] = None
    channelName: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigGQL:
    name: str
    windowPeriod: str
    series: List[CreateMetricConfigSeriesGQL]
    formulas: Optional[List[CreateMetricFormulaGQL]] = None
    trigger: Optional[CreateAlertTriggerGQL] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateChartGQL:
    id: str
    config: CreateMetricConfigGQL
    entityKind: str
    entityId: Optional[str] = None


class GraphLogSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclasses_json.dataclass_json
@dataclass
class UpdateGraphError:
    header: str
    subheader: str
    severity: GraphLogSeverity


@dataclasses_json.dataclass_json
@dataclass
class UpsertSQLSourceGQL:
    name: Optional[str]
    kind: str


@dataclasses_json.dataclass_json
@dataclass
class UpsertCDCSourceGQL:
    integrationName: str
    schemaDotTableList: List[str]


@dataclasses_json.dataclass_json
@dataclass
class FeatureClassGQL:
    isSingleton: bool
    doc: Optional[str]
    name: str
    owner: Optional[str]
    tags: List[str]


@dataclasses_json.dataclass_json
@dataclass
class UpsertGraphGQL:
    resolvers: Optional[List[UpsertResolverGQL]] = None
    features: Optional[List[UpsertFeatureGQL]] = None
    streams: Optional[List[UpsertStreamResolverGQL]] = None
    sinks: Optional[List[UpsertSinkResolverGQL]] = None
    charts: Optional[List[CreateChartGQL]] = None
    config: Optional[ProjectSettingsGQL] = None
    failed: Optional[List[FailedImport]] = None
    chalkpy: Optional[ChalkPYInfo] = None
    validated: Optional[bool] = None
    errors: Optional[List[UpdateGraphError]] = None
    cdcSources: Optional[List[UpsertCDCSourceGQL]] = None
    sqlSources: Optional[List[UpsertSQLSourceGQL]] = None
    featureClasses: Optional[List[FeatureClassGQL]] = None
