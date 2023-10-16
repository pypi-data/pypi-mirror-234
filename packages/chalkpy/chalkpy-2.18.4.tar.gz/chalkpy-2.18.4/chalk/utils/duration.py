from __future__ import annotations

import re
from datetime import timedelta
from re import Pattern
from typing import Literal, Mapping, Optional, Tuple, Union

from typing_extensions import TypeAlias

Duration: TypeAlias = Union[str, timedelta, Literal["infinity"]]
"""
Duration is used to describe time periods in natural language.
To specify using natural language, write the count of the unit
you would like, followed by the representation of the unit.

Chalk supports the following units:

 | Signifier | Meaning       |
 | --------- | ------------- |
 | w         | Weeks         |
 | d         | Days          |
 | h         | Hours         |
 | m         | Minutes       |
 | s         | Seconds       |
 | ms        | Milliseconds  |

As well as the special keyword `"infinity"`

Examples


| Signifier   | Meaning                           |
| ----------- | --------------------------------- |
| "10h"       | 10 hours                          |
| "1w 2m"     | 1 week and 2 minutes              |
| "1h 10m 2s" | 1 hour, 10 minutes, and 2 seconds |
| "infinity"  | Unbounded time duration           |

Read more at https://docs.chalk.ai/docs/duration
"""

CronTab: TypeAlias = str
"""
A schedule defined using the Unix-cron
string format (`* * * * *`).
Values are given in the order below:


| Field        | Values |
| ------------ | ------ |
| Minute       | 0-59   |
| Hour         | 0-23   |
| Day of Month | 1-31   |
| Month        | 1-12   |
| Day of Week  | 0-6    |
"""

ScheduleOptions: TypeAlias = Optional[Union[CronTab, Duration, Literal[True]]]
"""The schedule on which to run a resolver.

One of:
- `CronTab`: A Unix-cron string, e.g. `"* * * * *"`.
- `Duration`: A Chalk Duration, e.g. `"2h 30m"`.
- `True`: Used internally.
"""


def timedelta_to_duration(t: timedelta) -> str:
    if t == timedelta.max:
        return "infinity"
    s = ""
    if t.days > 0:
        s += f"{t.days}d"
    if t.seconds > 0:
        if len(s) > 0:
            s += " "
        s += f"{t.seconds}s"
    return s


_meaning_to_signifier = dict(weeks="w", days="d", hours="h", minutes="m", seconds="s", milliseconds="ms")

_kwarg_to_regex: Mapping[str, Pattern] = {
    k: re.compile(rf"(([0-9]+?){v}(?![a-z]))") for k, v in _meaning_to_signifier.items()
}


def parse_chalk_duration(s: str) -> timedelta:
    if s == "infinity" or s == "all":
        return timedelta.max

    def parse(regex: Pattern) -> Tuple[int, str]:
        matched = regex.search(s)
        if matched is None:
            return 0, ""

        return int(matched.groups()[1]), matched.groups()[0]

    parsed_values = {k: parse(unit) for k, unit in _kwarg_to_regex.items()}

    # Check for remaining unparsed input
    remainder = s
    for v in parsed_values.values():
        remainder = remainder.replace(v[1], "", 1)
    remainder = remainder.strip()

    if remainder != "":
        raise ValueError(f"Unparsed portion of duration: '{remainder}' for input: '{s}'")

    return timedelta(**{k: v[0] for k, v in parsed_values.items()})
