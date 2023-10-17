from typing import Mapping, Sequence, Union

__all__ = ["TJSON"]

TJSON = Union[None, str, int, float, bool, Sequence["TJSON"], Mapping[str, "TJSON"]]
