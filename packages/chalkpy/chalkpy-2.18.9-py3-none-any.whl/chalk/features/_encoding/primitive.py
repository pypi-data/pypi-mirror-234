from datetime import date, datetime, time, timedelta
from typing import Mapping, Sequence, Union

__all__ = ["TPrimitive"]

TPrimitive = Union[
    None,
    str,
    int,
    float,
    bool,
    date,
    datetime,
    time,
    timedelta,
    Sequence["TPrimitive"],
    Mapping[str, "TPrimitive"],
]
