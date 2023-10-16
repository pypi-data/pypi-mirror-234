import functools

from typing_extensions import get_type_hints


@functools.lru_cache(None)
def cached_get_type_hints(obj: type, include_extras: bool = False):
    return get_type_hints(obj, include_extras=include_extras)
