from __future__ import annotations

import collections.abc
import contextlib
import contextvars
import dataclasses
import threading
from datetime import datetime, timedelta, timezone
from types import TracebackType
from typing import TYPE_CHECKING, Any, Hashable, List, Set, Type

if TYPE_CHECKING:
    from chalk.features.feature_field import Feature


class Filter:
    def __init__(self, lhs: Any, operation: str, rhs: Any):
        from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature

        # Feature or other could be another feature, filter, featuretime, literal
        # Other could also be a sequence (in the case of operation = "in")
        self.operation = operation
        if isinstance(lhs, FeatureWrapper):
            lhs = unwrap_feature(lhs)
        self.lhs = lhs
        if self.operation == "in":
            if not isinstance(rhs, collections.abc.Iterable):
                raise ValueError("The RHS must be an iterable for operation='in'")
            rhs_unwrapped = [unwrap_feature(x) if isinstance(x, FeatureWrapper) else x for x in rhs]
            for x in rhs_unwrapped:
                if not isinstance(x, Hashable):
                    raise ValueError(f"RHS for operation='in' must be hashable; Found un-hashable type: {type(x)}")
            rhs = frozenset(unwrap_feature(x) if isinstance(x, FeatureWrapper) else x for x in rhs)
        else:
            if isinstance(rhs, FeatureWrapper):
                rhs = unwrap_feature(rhs)
        self.rhs = rhs

    def __hash__(self) -> int:
        return hash((self.lhs, self.operation, self.rhs))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Filter):
            return NotImplemented
        return self.lhs == other.lhs and self.operation == other.operation and self.rhs == other.rhs

    def __and__(self, other: object):
        return Filter(self, "and", other)

    def __or__(self, other: object):
        return Filter(self, "or", other)

    def __invert__(self):
        return Filter(self, "not", None)

    def referenced_features(self) -> Set[Feature]:
        from chalk.features.feature_field import Feature

        return {x for x in (self.lhs, self.rhs) if isinstance(x, Feature)}

    def __repr__(self):
        return f"Filter({self.lhs} {self.operation} {self.rhs})"


def _get_feature_time_index(explicit_index: Any):
    if explicit_index is None:
        from chalk.features.pseudofeatures import CHALK_TS_FEATURE

        return CHALK_TS_FEATURE

    from chalk.features.feature_wrapper import unwrap_feature

    return unwrap_feature(explicit_index)


@dataclasses.dataclass(frozen=True)
class TimeDelta:
    weeks_ago: int = 0
    days_ago: int = 0
    hours_ago: int = 0
    minutes_ago: int = 0
    seconds_ago: int = 0
    milliseconds_ago: int = 0
    microseconds_ago: int = 0

    def to_std(self) -> timedelta:
        # Returning the negative inverse since the feature is defined in the past (e.g. days **ago**)
        return -timedelta(
            weeks=self.weeks_ago,
            days=self.days_ago,
            hours=self.hours_ago,
            minutes=self.minutes_ago,
            seconds=self.seconds_ago,
            milliseconds=self.milliseconds_ago,
            microseconds=self.microseconds_ago,
        )


def before(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
    index: Any = None,
) -> Any:
    """The function `before` can be used with `DataFrame` to compute windowed features.

    Before filters a `DataFrame` relative to the current time in context.
    This time could be in the past if you’re using an offline resolver.
    Using window functions ensures that you maintain point-in-time correctness.

    The parameters to `before` take many keyword arguments describing the
    time relative to the present.

    Parameters
    ----------
    days_ago
        Number of days ago.
    hours_ago
        Number of hours ago.
    minutes_ago
        Number of minutes ago.
    seconds_ago
        Number of seconds ago.
    index
        The feature to use for the filter. By default, `index` is the `FeatureTime`
        of the referenced feature class.

    Other Parameters
    ----------------
    weeks_ago
        Number of weeks ago.
    milliseconds_ago
        Number of milliseconds ago.
    microseconds_ago
        Number of microseconds ago.

    Returns
    -------
    Any
        A filter for a `DataFrame`.

    Examples
    --------
    >>> from chalk.features import DataFrame, features
    >>> @features
    ... class Card:
    ...     ...
    >>> @features
    ... class User:
    ...     cards: DataFrame[Card]
    >>> User.cards[before(hours_ago=1, minutes_ago=30)]
    """
    return Filter(
        lhs=_get_feature_time_index(index),
        operation="<=",
        rhs=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )


def after(
    weeks_ago: int = 0,
    days_ago: int = 0,
    hours_ago: int = 0,
    minutes_ago: int = 0,
    seconds_ago: int = 0,
    milliseconds_ago: int = 0,
    microseconds_ago: int = 0,
    index: Any = None,
) -> Any:
    """The function `after` can be used with `DataFrame` to compute windowed features.

    After filters a `DataFrame` relative to the current time in context.
    This time could be in the past if you’re using an offline resolver.
    Using window functions ensures that you maintain point-in-time correctness.

    The parameters to `after` take many keyword arguments describing the
    time relative to the present.

    Parameters
    ----------
    days_ago
        Number of days ago.
    hours_ago
        Number of hours ago.
    minutes_ago
        Number of minutes ago.
    seconds_ago
        Number of seconds ago.
    index
        The feature to use for the filter. By default, `index` is the `FeatureTime`
        of the referenced feature class.

    Other Parameters
    ----------------
    weeks_ago
        Number of weeks ago.
    milliseconds_ago
        Number of milliseconds ago.
    microseconds_ago
        Number of microseconds ago.

    Returns
    -------
    Any
        A filter for the `DataFrame`.

    Examples
    --------
    >>> from chalk.features import DataFrame, features
    >>> @features
    ... class Card:
    ...     ...
    >>> @features
    ... class User:
    ...     cards: DataFrame[Card]
    >>> User.cards[after(hours_ago=1, minutes_ago=30)]
    """
    return Filter(
        lhs=_get_feature_time_index(index),
        operation=">=",
        rhs=TimeDelta(
            weeks_ago=weeks_ago,
            days_ago=days_ago,
            hours_ago=hours_ago,
            minutes_ago=minutes_ago,
            seconds_ago=seconds_ago,
            milliseconds_ago=milliseconds_ago,
            microseconds_ago=microseconds_ago,
        ),
    )


_FILTER_NOW_CONTEXT_STACK: contextvars.ContextVar[datetime] = contextvars.ContextVar("_FILTER_NOW_CONTEXT_STACK")


def _get_filter_now() -> datetime:
    return _FILTER_NOW_CONTEXT_STACK.get(datetime.now(tz=timezone.utc))


class freeze_time(contextlib.AbstractContextManager):
    """
    Used to freeze the 'now' value used to execute filters like 'after(days_ago=7).

    The `at` parameter must be timezone aware.
    """

    def __init__(self, at: datetime):
        if at.tzinfo is None:
            raise ValueError("Timestamps used with 'freeze_time' must have timezone information associated with them.")
        self._time = at
        # Keep a list of previous contextvar tokens so that this context manager is re-entrant
        # (i.e. you can enter multiple times and then exit multiple times)
        self._token_stack = []

    def time(self) -> datetime:
        return self._time

    def __enter__(self):
        token = _FILTER_NOW_CONTEXT_STACK.set(self._time)
        self._token_stack.append(token)
        return self

    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        previous_token = self._token_stack.pop(-1)
        _FILTER_NOW_CONTEXT_STACK.reset(previous_token)
        return None


__all__ = [
    "Filter",
    "TimeDelta",
    "after",
    "before",
]
