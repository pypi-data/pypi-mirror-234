from typing import Union

from chalk._monitoring.Chart import (
    AlertSeverityKind,
    Chart,
    MetricFormulaKind,
    SeriesBase,
    ThresholdPosition,
    Trigger,
    _DatasetFeatureOperand,
    _Formula,
    _MultiSeriesOperand,
    _SingleSeriesOperand,
)
from chalk._monitoring.charts_enums_codegen import (
    ComparatorKind,
    FilterKind,
    GroupByKind,
    MetricKind,
    WindowFunctionKind,
)
from chalk._monitoring.charts_series_base import MetricFilter
from chalk.parsed.duplicate_input_gql import (
    AlertSeverityKindGQL,
    ComparatorKindGQL,
    CreateAlertTriggerGQL,
    CreateChartGQL,
    CreateDatasetFeatureOperandGQL,
    CreateMetricConfigGQL,
    CreateMetricConfigSeriesGQL,
    CreateMetricFilterGQL,
    CreateMetricFormulaGQL,
    FilterKindGQL,
    GroupByKindGQL,
    MetricFormulaKindGQL,
    MetricKindGQL,
    ThresholdKindGQL,
    WindowFunctionKindGQL,
)


def _convert_series(series: SeriesBase) -> CreateMetricConfigSeriesGQL:
    return CreateMetricConfigSeriesGQL(
        metric=convert_metric_kind(series._metric),
        filters=[_convert_filter(series_filter) for series_filter in series._filters],
        name=series._name or series._default_name,
        windowFunction=_convert_window_function(series._window_function),
        groupBy=[_convert_group_by(group_by) for group_by in series._group_by],
    )


def convert_metric_kind(metric_kind: Union[MetricKind, None]) -> MetricKindGQL:
    if not metric_kind:
        raise ValueError("'metric' is a required value for Series instances")
    return MetricKindGQL(metric_kind.value.upper())


def _convert_filter(filter: MetricFilter) -> CreateMetricFilterGQL:
    return CreateMetricFilterGQL(
        kind=_convert_filter_kind(filter.kind),
        comparator=_convert_comparator_kind(filter.comparator),
        value=filter.value,
    )


def _convert_filter_kind(filter_kind: FilterKind) -> FilterKindGQL:
    return FilterKindGQL(filter_kind.value.upper())


def _convert_comparator_kind(comparator_kind: ComparatorKind) -> ComparatorKindGQL:
    return ComparatorKindGQL(comparator_kind.value.upper())


def _convert_window_function(window_function: Union[WindowFunctionKind, None]) -> Union[WindowFunctionKindGQL, None]:
    if not window_function:
        return None
    return WindowFunctionKindGQL(window_function.value.upper())


def _convert_group_by(group_by: GroupByKind) -> GroupByKindGQL:
    return GroupByKindGQL(group_by.value.upper())


def _convert_formula(formula: _Formula) -> CreateMetricFormulaGQL:
    operands = formula._operands
    if not operands:
        raise ValueError("'operands' is a required value for Formula instances")
    single_series = None
    multi_series = None
    dataset_feature = None
    if isinstance(operands, _SingleSeriesOperand):
        single_series = operands.operand
    elif isinstance(operands, _MultiSeriesOperand):
        multi_series = operands.operands
    elif isinstance(operands, _DatasetFeatureOperand):
        dataset_feature = CreateDatasetFeatureOperandGQL(dataset=operands.dataset, feature=operands.feature)
    if not single_series and not multi_series and not dataset_feature:
        raise ValueError(f"'operands' value '{operands}' is not of a valid type for Formula instances")
    return CreateMetricFormulaGQL(
        kind=_convert_metric_formula_kind(formula._kind),
        singleSeriesOperands=single_series,
        multiSeriesOperands=multi_series,
        datasetFeatureOperands=dataset_feature,
        name=formula._name,
    )


def _convert_metric_formula_kind(kind: Union[MetricFormulaKind, None]) -> MetricFormulaKindGQL:
    if not kind:
        raise ValueError("'kind' is a required value for Formula instances")
    return MetricFormulaKindGQL(kind.value.upper())


def _convert_trigger(trigger: Trigger) -> CreateAlertTriggerGQL:
    if not trigger._name:
        raise ValueError("'name' is a required value for Trigger instances")
    if not trigger._threshold_value:
        raise ValueError("'threshold_value' is a required value for Trigger instances")
    return CreateAlertTriggerGQL(
        name=trigger._name,
        severity=_convert_severity(trigger._severity),
        thresholdPosition=_convert_threshold_position(trigger._threshold_position),
        thresholdValue=trigger._threshold_value,
        seriesName=trigger._series_name,
        channelName=trigger._channel_name,
    )


def _convert_severity(severity: Union[AlertSeverityKind, None]) -> AlertSeverityKindGQL:
    if not severity:
        raise ValueError("'severity' is a required value for Trigger instances")
    return AlertSeverityKindGQL(severity.value.lower())  # this GQL Enum object is the only in lowercase


def _convert_threshold_position(threshold_position: Union[ThresholdPosition, None]) -> ThresholdKindGQL:
    if not threshold_position:
        raise ValueError("'threshold_position' is a required value for Trigger instances")
    return ThresholdKindGQL(threshold_position.value.upper())


def convert_chart(chart: Chart) -> CreateChartGQL:
    if not chart._window_period:
        raise ValueError("'window_period' is a required value for Chart instances")
    config = CreateMetricConfigGQL(
        name=chart._name,
        windowPeriod=chart._window_period,
        series=[_convert_series(series) for series in chart._series],
        formulas=[_convert_formula(formula) for formula in chart._formulas],
        trigger=_convert_trigger(chart._trigger) if chart._trigger else None,
    )
    return CreateChartGQL(
        id=str(hash(chart)),
        config=config,
        entityKind=chart._entity_kind.value,
        entityId=chart._entity_id,
    )
