import contextlib
from typing import AsyncIterator, TypeVar

T = TypeVar("T")


@contextlib.asynccontextmanager
async def async_null_context(obj: T) -> AsyncIterator[T]:
    yield obj
