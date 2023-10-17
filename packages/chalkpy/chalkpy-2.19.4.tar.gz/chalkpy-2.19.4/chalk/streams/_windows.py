from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, Generic, Iterable, List, Mapping, Optional, Set, Type, TypeVar, Union, cast

from chalk._validation.feature_validation import FeatureValidation
from chalk._validation.validation import Validation
from chalk.features._encoding.primitive import TPrimitive
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import Duration, parse_chalk_duration

TPrim = TypeVar("TPrim", bound=TPrimitive)
TRich = TypeVar("TRich")

if TYPE_CHECKING:
    import pyarrow as pa

    from chalk.features._encoding.converter import TDecoder, TEncoder


class WindowedInstance(Generic[TRich]):
    def __init__(self, values: Mapping[str, TRich]):
        self.values = values

    def __call__(self, period: str):
        return self.values[period]


class WindowedMeta(type, Generic[TRich]):
    def __getitem__(cls, underlying: Type[TRich]) -> Windowed[TRich]:
        return Windowed(
            kind=underlying,
            buckets=[],
            description=None,
            owner=None,
            tags=None,
            name=None,
            default=...,
            max_staleness=None,
            version=None,
            etl_offline_to_online=None,
            encoder=None,
            decoder=None,
            min=None,
            max=None,
            min_length=None,
            max_length=None,
            contains=None,
            strict=False,
            dtype=None,
            validations=None,
            offline_ttl=None,
        )  # noqa


JsonValue = Any


def get_duration_secs(duration: Union[str, int, timedelta]) -> int:
    if isinstance(duration, str):
        duration = parse_chalk_duration(duration)
    if isinstance(duration, timedelta):
        duration_secs_float = duration.total_seconds()
        duration_secs_int = int(duration_secs_float)
        if duration_secs_float != duration_secs_int:
            raise ValueError("Windows that are fractions of seconds are not yet supported")
        duration = duration_secs_int
    return duration


# 100 years == "all"
MAX_WINDOW_BUCKET_SECONDS = 100 * 365 * 24 * 60 * 60


def get_name_with_duration(name_or_fqn: str, duration: Union[str, int, timedelta]) -> str:
    duration_secs = get_duration_secs(duration)
    if duration_secs > MAX_WINDOW_BUCKET_SECONDS:
        return f"{name_or_fqn}__all__"
    else:
        return f"{name_or_fqn}__{duration_secs}__"


if TYPE_CHECKING:
    _WINDOWED_METACLASS = type
else:
    _WINDOWED_METACLASS = WindowedMeta


class Windowed(Generic[TRich], metaclass=_WINDOWED_METACLASS):
    """Declare a windowed feature.

    Examples
    --------
    >>> @features
    ... class User:
    ...     failed_logins: Windowed[int] = windowed("10m", "24h")
    """

    def __getitem__(self, item):
        # Here for editor support
        super().__getitem__(item)

    @property
    def buckets_seconds(self) -> Set[int]:
        return set(int(parse_chalk_duration(bucket).total_seconds()) for bucket in self._buckets)

    @property
    def kind(self) -> Type[TRich]:
        if self._kind is None:
            raise RuntimeError("Window type has not yet been parsed")
        return self._kind

    @kind.setter
    def kind(self, kind: Type[TRich]) -> None:
        assert self._kind is None, "Window type cannot be set twice"
        self._kind = kind

    def _to_feature(self, bucket: Optional[Union[int, str]]):
        from chalk.features import Feature

        assert self._name is not None

        if bucket is None:
            name = self._name
        elif get_duration_secs(bucket) not in self.buckets_seconds:
            raise ValueError(f"Bucket {bucket} is not in the list of specified buckets")
        else:
            name = get_name_with_duration(self._name, bucket)

        return Feature(
            name=name,
            version=self._version,
            owner=self._owner,
            tags=None if self._tags is None else list(ensure_tuple(self._tags)),
            description=self._description,
            primary=False,
            default=self._default,
            max_staleness=self._max_staleness,
            offline_ttl=self._offline_ttl,
            etl_offline_to_online=self._etl_offline_to_online,
            encoder=self._encoder,
            decoder=self._decoder,
            pyarrow_dtype=self._dtype,
            validations=FeatureValidation(
                min=self._min,
                max=self._max,
                min_length=self._min_length,
                max_length=self._max_length,
                contains=self._contains,
                strict=self._strict,
            ),
            all_validations=None
            if self._validations is None
            else [
                FeatureValidation(
                    min=v.min,
                    max=v.max,
                    min_length=v.min_length,
                    max_length=v.max_length,
                    contains=None,
                    strict=v.strict,
                )
                for v in self._validations
            ],
            # Only the root feature should have all the durations
            # The pseudofeatures, which are bound to a duration, should not have the durations
            # of the other buckets
            window_durations=tuple(self.buckets_seconds) if bucket is None else tuple(),
            window_duration=None if bucket is None else get_duration_secs(bucket),
        )

    def __init__(
        self,
        buckets: List[str],
        description: Optional[str],
        owner: Optional[str],
        tags: Optional[Any],
        name: Optional[str],
        default: Union[TRich, ellipsis],
        max_staleness: Optional[Union[Duration, ellipsis]],
        version: Optional[int],
        etl_offline_to_online: Optional[bool],
        encoder: Optional[TEncoder[TPrim, TRich]],
        decoder: Optional[TDecoder[TPrim, TRich]],
        min: Optional[TRich],
        max: Optional[TRich],
        min_length: Optional[int],
        max_length: Optional[int],
        contains: Optional[TRich],
        strict: bool,
        validations: Optional[List[Validation]],
        dtype: Optional[pa.DataType],
        kind: Optional[Type[TRich]],
        offline_ttl: Optional[Union[Duration, ellipsis]],
    ):
        self._kind = kind
        self._name: Optional[str] = None
        self._buckets = buckets
        self._description = description
        self._owner = owner
        self._tags = tags
        self._name = name
        self._default = default
        self._max_staleness = max_staleness
        self._offline_ttl = offline_ttl
        self._description = description
        self._version = version
        self._etl_offline_to_online = etl_offline_to_online
        self._encoder = encoder
        self._decoder = decoder
        self._min = min
        self._max = max
        self._min_length = min_length
        self._max_length = max_length
        self._contains = contains
        self._strict = strict
        self._validations = validations
        self._dtype = dtype


class SelectedWindow:
    def __init__(self, kind: Windowed, selected: str):
        self.windowed = kind
        self.selected = selected


def windowed(
    *buckets: str,
    days: Iterable[int, ...] = (),
    hours: Iterable[int, ...] = (),
    minutes: Iterable[int, ...] = (),
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Any] = None,
    name: Optional[str] = None,
    default: Union[TRich, ellipsis] = ...,
    max_staleness: Optional[Union[Duration, ellipsis]] = ...,
    offline_ttl: Optional[Union[Duration, ellipsis]] = ...,
    version: Optional[int] = None,
    etl_offline_to_online: Optional[bool] = None,
    encoder: Optional[TEncoder[TPrim, TRich]] = None,
    decoder: Optional[TDecoder[TPrim, TRich]] = None,
    min: Optional[TRich] = None,
    max: Optional[TRich] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    strict: bool = False,
    validations: Optional[List[Validation]] = None,
    dtype: Optional[pa.DataType] = None,
) -> Windowed[TRich]:
    """Create a windowed feature.

    See more at https://docs.chalk.ai/docs/aggregations#windowed-features

    Parameters
    ----------
    buckets
        The size of the buckets for the window function.
        Buckets are specified as strings in the format `"1d"`, `"2h"`, `"1h30m"`, etc.
        You may also choose to specify the buckets using the days, hours, and minutes
        parameters instead. The buckets parameter is helpful if you want to use
        multiple units to express the bucket size, like `"1h30m"`.
    days
        Convenience parameter for specifying the buckets in days.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1d"`.
    hours
        Convenience parameter for specifying the buckets in hours.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1h"`.
    minutes
        Convenience parameter for specifying the buckets in minutes.
        Using this parameter is equvalent to specifying the buckets parameter
        with a string like `"1m"`.
    default
        The default value of the feature if it otherwise can't be computed.
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.

        Read more at https://docs.chalk.ai/docs/feature-caching
    version
        Feature versions allow you to manage a feature as its
        definition changes over time.

        The `version` keyword argument allows you to specify the
        maximum number of versions available for this feature.

        See more at https://docs.chalk.ai/docs/feature-versions
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.

        Read more at https://docs.chalk.ai/docs/reverse-etl
    min
        If specified, when this feature is computed, Chalk will check that `x >= min`.
    max
        If specified, when this feature is computed, Chalk will check that `x <= max`.
    min_length
        If specified, when this feature is computed, Chalk will check that `len(x) >= min_length`.
    max_length
        If specified, when this feature is computed, Chalk will check that `len(x) <= max_length`.
    strict
        If `True`, if this feature does not meet the validation criteria, Chalk will not persist
        the feature value and will treat it as failed.
    validations
    offline_ttl

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `email_count` feature with information about the values
        as follows::
        >>> @features
        ... class User:
        ...     # Count of emails sent
        ...     email_count: Windowed[int] = windowed("10m", "30m")

        You can also specify the description directly with this parameter.
        >>> @features
        ... class User:
        ...     email_count: Windowed[int] = windowed(
        ...         "10m", "30m"
        ...         description="Count of emails sent",
        ...     )
    encoder
    decoder
    dtype

    Returns
    -------
    Windowed[TPrim, TRich]
        Metadata for the windowed feature, parameterized by
        `TPrim` (the primitive type of the feature) and
        `TRich` (the decoded type of the feature, if `decoder` is provided).

    Examples
    --------
    >>> from chalk import windowed, Windowed
    >>> @features
    ... class User:
    ...     id: int
    ...     email_count: Windowed[int] = windowed(days=range(1, 30))
    ...     logins: Windowed[int] = windowed("10m", "1d", "30d")
    >>> User.email_count["7d"]
    """
    return Windowed(
        list(buckets) + [f"{x}m" for x in minutes] + [f"{x}h" for x in hours] + [f"{x}d" for x in days],
        description=description,
        owner=owner,
        tags=tags,
        name=name,
        default=default,
        max_staleness=max_staleness,
        version=version,
        etl_offline_to_online=etl_offline_to_online,
        encoder=cast("TEncoder", encoder),
        decoder=decoder,
        min=min,
        max=max,
        min_length=min_length,
        max_length=max_length,
        contains=None,
        strict=strict,
        dtype=dtype,
        kind=None,
        validations=validations,
        offline_ttl=offline_ttl,
    )
