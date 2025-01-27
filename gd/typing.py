from abc import abstractmethod
from builtins import hasattr as has_attribute
from builtins import isinstance as is_instance
from inspect import isawaitable as standard_is_awaitable
from os import PathLike
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Protocol, TypeAlias, TypeGuard, runtime_checkable
from yarl import URL

__all__ = (
    "AnyType",
    "DynamicCallable",
    "AnyCallable",
    "AnyException",
    "AnyIterable",
    "Nullary",
    "Unary",
    "Binary",
    "Ternary",
    "Quaternary",
    "ClassDecorator",
    "ClassDecoratorIdentity",
    "Decorator",
    "DecoratorIdentity",
    "Predicate",
    "Parse",
    "DynamicTuple",
    "MaybeIterable",
    "StringDict",
    "StringMapping",
    "Namespace",
    "IntoPath",
    "JSONType",
    "is_same_type",
    "is_iterable",
    "is_string",
    "is_error",
    "Named",
    "is_named",
    "get_name",
    "HasModule",
    "has_module",
    "get_module",
    "is_instance",
)

AnyType = Type[Any]

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")

DynamicCallable = Callable[..., R]
AnyCallable = DynamicCallable[Any]

AnyException: TypeAlias = BaseException
AnyExceptionType: TypeAlias = Type[AnyException]

Nullary = Callable[[], R]
Unary = Callable[[T], R]
Binary = Callable[[T, U], R]
Ternary = Callable[[T, U, V], R]
Quaternary = Callable[[T, U, V, W], R]

AsyncNullary = Nullary[Awaitable[R]]
AsyncUnary = Unary[T, Awaitable[R]]
AsyncBinary = Binary[T, U, Awaitable[R]]
AsyncTernary = Ternary[T, U, V, Awaitable[R]]
AsyncQuaternary = Quaternary[T, U, V, W, Awaitable[R]]

C = TypeVar("C", bound=AnyType)
D = TypeVar("D", bound=AnyType)

ClassDecorator = Unary[C, D]
ClassDecoratorIdentity = ClassDecorator[C, C]

F = TypeVar("F", bound=AnyCallable)
G = TypeVar("G", bound=AnyCallable)

Decorator = Unary[F, G]
DecoratorIdentity = Decorator[F, F]

Predicate = Unary[T, bool]
Parse = Unary[str, T]

DynamicTuple = Tuple[T, ...]

MaybeIterable = Union[Iterable[T], T]

AnyIterable = Union[AsyncIterable[T], Iterable[T]]

StringDict = Dict[str, T]
StringMapping = Mapping[str, T]

Namespace = StringDict[Any]

Parameters = StringMapping[Any]
Headers = StringMapping[Any]

IntString = Union[str, int]
URLString = Union[str, URL]

Pairs = Iterable[Tuple[T, U]]

IntoMapping = Union[Mapping[T, U], Pairs[T, U]]

IntoStringMapping = IntoMapping[str, T]

IntoNamespace = IntoStringMapping[Any]

IntoParameters = IntoStringMapping[Any]

MaybeMapping = Union[Mapping[T, U], V]

try:
    IntoPath = Union[str, PathLike[str]]  # type: ignore

except TypeError:
    IntoPath = Union[str, PathLike]  # type: ignore


JSONType: TypeAlias = Optional[Union[bool, int, float, str, StringDict[Any], List[Any]]]


LT = TypeVar("LT", bound="Less")


@runtime_checkable
class Less(Protocol):
    @abstractmethod
    def __lt__(self: LT, other: LT) -> bool:
        ...


GT = TypeVar("GT", bound="Greater")


@runtime_checkable
class Greater(Protocol):
    @abstractmethod
    def __lt__(self: GT, other: GT) -> bool:
        ...


StrictOrdered = Union[Less, Greater]


def is_same_type(value: Any, item: T) -> TypeGuard[T]:
    return type(value) is type(item)


def is_iterable(maybe_iterable: MaybeIterable[T]) -> TypeGuard[Iterable[T]]:
    return is_instance(maybe_iterable, Iterable)


def is_mapping(maybe_mapping: MaybeMapping[T, U, V]) -> TypeGuard[Mapping[T, U]]:
    return is_instance(maybe_mapping, Mapping)


def is_bytes(item: Any) -> TypeGuard[bytes]:
    return is_instance(item, bytes)


def is_string(item: Any) -> TypeGuard[str]:
    return is_instance(item, str)


def is_error(item: Any) -> TypeGuard[AnyException]:
    return is_instance(item, AnyException)


@runtime_checkable
class Named(Protocol):
    __name__: str


NAME = "__name__"


def is_named(item: Any) -> TypeGuard[Named]:
    return has_attribute(item, NAME)


def get_name(item: Named) -> str:
    return item.__name__


@runtime_checkable
class HasModule(Protocol):
    __module__: str


MODULE = "__module__"


def has_module(item: Any) -> TypeGuard[HasModule]:
    return has_attribute(item, MODULE)


def get_module(item: HasModule) -> str:
    return item.__module__
