from functools import wraps

from gd.async_utils import maybe_coroutine
from gd.typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Generic,
    Generator,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)

__all__ = ("AsyncIter", "async_iter", "async_iterable", "iter_to_async_iter")

T = TypeVar("T")
U = TypeVar("U")


async def iter_to_async_iter(iterable: Iterable[T]) -> AsyncIterator[T]:
    for item in iterable:
        yield item


class AsyncIter(Generic[T]):
    def __init__(self, iterable: Union[AsyncIterable[T], Iterable[T]]) -> None:
        if isinstance(iterable, Iterable):
            self.iterator = iter_to_async_iter(iterable).__aiter__()

        elif isinstance(iterable, AsyncIterable):
            self.iterator = iterable.__aiter__()

        else:
            raise TypeError(f"Object of type {type(iterable).__name__!r} is not iterable.")

    def __aiter__(self) -> "AsyncIter[T]":  # XXX: should we expose inner iterator?
        return self

    def __await__(self) -> Generator[Any, None, List[T]]:
        # transform: await async_iter -> await async_iter.flatten()
        return self.flatten().__await__()

    async def __anext__(self) -> T:
        return await self.iterator.__anext__()

    async def next(self) -> T:
        return await self.iterator.__anext__()

    async def get(self, **attrs) -> Optional[T]:
        def predicate(item: T) -> bool:
            for attr, value in attrs.items():
                nested = attr.split("__")

                actual_item = item

                for attribute in nested:
                    actual_item = getattr(actual_item, attribute)

                if actual_item != value:
                    return False

            return True

        return await self.find(predicate)

    async def find(self, predicate: Callable[[T], Union[bool, Awaitable[bool]]]) -> Optional[T]:
        async for item in self.iterator:
            if await maybe_coroutine(predicate, item):
                return item
        return None

    async def map_iter(self, function: Callable[[T], Union[U, Awaitable[U]]]) -> AsyncIterator[U]:
        async for item in self.iterator:
            yield await maybe_coroutine(function, item)

    async def filter_iter(
        self, predicate: Callable[[T], Union[bool, Awaitable[bool]]]
    ) -> AsyncIterator[T]:
        async for item in self.iterator:
            if await maybe_coroutine(predicate, item):
                yield item

    async def map(self, function: Callable[[T], Union[U, Awaitable[U]]]) -> "AsyncIter[U]":
        return self.__class__(self.map_iter(function))

    async def filter(
        self, predicate: Callable[[T], Union[bool, Awaitable[bool]]]
    ) -> "AsyncIter[T]":
        return self.__class__(self.filter_iter(predicate))

    async def flatten(self) -> List[T]:
        return [item async for item in self.iterator]


def async_iter(iterable: Union[AsyncIterable[T], Iterable[T]]) -> AsyncIter[T]:
    return AsyncIter(iterable)


def async_iterable(
    function: Callable[..., Union[AsyncIterable[T], Iterable[T]]]
) -> Callable[..., AsyncIter[T]]:
    @wraps(function)
    def wrapper(*args, **kwargs) -> AsyncIter[T]:
        return async_iter(function(*args, **kwargs))

    return wrapper