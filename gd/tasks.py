"""..., adapted from `discord.py` library."""

from __future__ import annotations

from asyncio import CancelledError, Task, TimeoutError, create_task, sleep
from builtins import issubclass as is_subclass
from functools import partial
from random import Random
from time import monotonic as clock
from typing import Any, Awaitable, Callable, Generic, Optional, Type, TypeVar, Union

from aiohttp import ClientError
from attrs import define, field
from typing_extensions import ParamSpec

from gd.errors import GDError
from gd.typing import AnyException, DynamicTuple, Nullary, StringDict, Unary

__all__ = ("ExponentialBackoff", "Loop", "loop")

Clock = Nullary[float]

DAYS_TO_HOURS = 24.0
HOURS_TO_MINUTES = 60.0
MINUTES_TO_SECONDS = 60.0
HOURS_TO_SECONDS = HOURS_TO_MINUTES * MINUTES_TO_SECONDS
DAYS_TO_MINUTES = DAYS_TO_HOURS * HOURS_TO_MINUTES
DAYS_TO_SECONDS = DAYS_TO_MINUTES * MINUTES_TO_SECONDS

RANDOM = Random()
RANDOM.seed()

uniform_to = partial(RANDOM.uniform, 0.0)

DEFAULT_MULTIPLY = 1.0
DEFAULT_BASE = 2.0
DEFAULT_LIMIT = 10


@define()
class ExponentialBackoff:
    r"""An implementation of the *exponential backoff* algorithm.

    Provides a convenient interface to implement an exponential backoff
    for reconnecting or retrying transmissions in a distributed network.

    Once instantiated, the delay method will return the next interval to
    wait for when retrying a connection or transmission. The maximum
    delay increases exponentially with each retry up to a maximum of
    $m \cdot b^l$ (where $m$ is `multiply`, $b$ is `base` and $l$ is `limit`),
    and is reset if no more attempts are needed in a period of $m \cdot b^{l + 1}$ seconds.
    """

    multiply: float = field(default=DEFAULT_MULTIPLY)
    base: float = field(default=DEFAULT_BASE)
    limit: int = field(default=DEFAULT_LIMIT)

    _clock: Clock = field(default=clock)

    _exponent: int = field(default=0, init=False)
    _last_called: float = field(init=False)
    _reset_delta: float = field(init=False)

    @_last_called.default
    def default_last_called(self) -> float:
        return self._clock()

    @_reset_delta.default
    def default_reset_delta(self) -> float:
        return self.multiply * pow(self.base, self.limit + 1)

    def delay(self) -> float:
        r"""Computes the next delay.

        Returns the next delay to wait according to the exponential
        backoff algorithm. This is a value between $0$ and $m \cdot b ^ e$
        where $e$ (`exponent`) starts off at $0$ and is incremented at every
        invocation of this method up to a maximum of $l$ (`limit`).

        If a period of more than $m \cdot b^{l + 1}$ has passed since the last
        retry, the `exponent` ($e$) is reset to $0$.
        """
        called = self._clock()

        interval = called - self._last_called
        self._last_called = called

        if interval > self._reset_delta:
            self._exponent = 0

        if self._exponent < self.limit:
            self._exponent += 1

        return uniform_to(self.multiply * pow(self.base, self._exponent))


P = ParamSpec("P")
S = TypeVar("S")

LoopFunction = Union[Nullary[Awaitable[None]], Unary[S, Awaitable[None]]]

TASK_ALREADY_LAUNCHED = "task is already launched and has not completed yet"

DEFAULT_DELAY = 0.0
DEFAULT_RECONNECT = True

F = TypeVar("F", bound=LoopFunction[Any])
L = TypeVar("L", bound="Loop[Any]")


@define()
class Loop(Generic[P]):
    """A background task helper that abstracts the loop and reconnection logic.

    The main interface to create this is through [`loop`][gd.tasks.loop].
    """

    function: Callable[P, Awaitable[None]] = field()

    delay: float = field(default=DEFAULT_DELAY)

    count: Optional[int] = field(default=None)

    reconnect: bool = field(default=DEFAULT_RECONNECT)

    _task: Optional[Task[None]] = field(default=None, init=False)

    _current_count: int = field(default=0, init=False)

    _error_types: DynamicTuple[Type[AnyException]] = field(
        default=(OSError, GDError, ClientError, TimeoutError),
        init=False,
    )

    _is_being_cancelled: bool = field(default=False, init=False)
    _has_failed: bool = field(default=False, init=False)
    _stop_next_iteration: bool = field(default=False, init=False)

    _injected: Optional[Any] = field(default=None, init=False)

    _before_loop: Optional[LoopFunction[Any]] = field(default=None, init=False)
    _after_loop: Optional[LoopFunction[Any]] = field(default=None, init=False)

    async def _call_before_loop(self) -> None:
        before_loop = self._before_loop

        if before_loop is None:
            return

        injected = self._injected

        if injected is None:
            await before_loop()  # type: ignore

        else:
            await before_loop(injected)  # type: ignore

    async def _call_after_loop(self) -> None:
        after_loop = self._after_loop

        if after_loop is None:
            return

        injected = self._injected

        if injected is None:
            await after_loop()  # type: ignore

        else:
            await after_loop(injected)  # type: ignore

    async def _loop(self, *args: P.args, **kwargs: P.kwargs) -> None:
        backoff = ExponentialBackoff()

        await self._call_before_loop()

        try:
            while True:
                try:
                    await self.function(*args, **kwargs)

                except self._error_types:

                    if not self.reconnect:
                        raise

                    await sleep(backoff.delay())

                else:
                    if self._stop_next_iteration:
                        return

                    self._current_loop += 1

                    if self._current_loop == self.count:
                        break

                    await sleep(self.delay)

        except CancelledError:
            self._is_being_cancelled = True

            raise

        except Exception:
            self._has_failed = True

            raise

        finally:
            await self._call_after_loop()

            self._current_loop = 0

            self._is_being_cancelled = False
            self._has_failed = False
            self._stop_next_iteration = False

    def __get__(self: L, instance: Optional[S], type: Optional[Type[S]] = None) -> L:
        if instance is None:
            return self

        self._injected = instance

        return self

    @property
    def current_loop(self) -> int:
        return self._current_loop

    def start(self, *args: Any, **kwargs: Any) -> Task[None]:
        task = self._task

        if task is not None and not task.done():
            raise RuntimeError(TASK_ALREADY_LAUNCHED)

        injected = self._injected

        if injected is not None:
            args = (injected, *args)

        self._task = task = create_task(self._loop(*args, **kwargs))

        return task

    def stop(self) -> None:
        task = self._task

        if task is not None and not task.done():
            self._stop_next_iteration = True

    @property
    def _can_be_cancelled(self) -> bool:
        task = self._task

        return not self._is_being_cancelled and task is not None and not task.done()

    def cancel(self) -> None:
        if self._can_be_cancelled:
            self._task.cancel()  # type: ignore

    def restart(self, *args: Any, **kwargs: Any) -> None:
        def restart_when_over(
            task: Task[None],
            *,
            args: DynamicTuple[Any] = args,
            kwargs: StringDict[Any] = kwargs,
        ) -> None:
            self._task.remove_done_callback(restart_when_over)  # type: ignore
            self.start(*args, **kwargs)

        if self._can_be_cancelled:
            self._task.add_done_callback(restart_when_over)  # type: ignore
            self._task.cancel()  # type: ignore

    def add_error_type(self, error_type: Type[AnyException]) -> None:
        if not is_subclass(error_type, AnyException):
            raise TypeError  # TODO: message?

        self._error_types = (*self._error_types, error_type)

    def clear_error_types(self) -> None:
        self._error_types = ()

    def remove_error_type(self, error_type: Type[AnyException]) -> bool:
        error_types = self._error_types

        length = len(error_types)

        self._error_types = error_types = tuple(
            present_error_type
            for present_error_type in error_types
            if present_error_type is not error_type
        )

        return len(error_types) < length

    def is_being_cancelled(self) -> bool:
        return self._is_being_cancelled

    def has_failed(self) -> bool:
        return self._has_failed

    def before_loop(self, loop_function: F) -> F:
        self._before_loop = loop_function

        return loop_function

    def after_loop(self, loop_function: F) -> F:
        self._after_loop = loop_function

        return loop_function


DEFAULT_SECONDS = 0.0
DEFAULT_MINUTES = 0.0
DEFAULT_HOURS = 0.0
DEFAULT_DAYS = 0.0


def loop(
    *,
    seconds: float = DEFAULT_SECONDS,
    minutes: float = DEFAULT_MINUTES,
    hours: float = DEFAULT_HOURS,
    days: float = DEFAULT_DAYS,
    count: Optional[int] = None,
    reconnect: bool = DEFAULT_RECONNECT,
) -> Unary[Callable[P, Awaitable[None]], Loop[P]]:
    """..."""

    delay = (
        seconds + minutes * MINUTES_TO_SECONDS + hours * HOURS_TO_SECONDS + days * DAYS_TO_SECONDS
    )

    def wrap(function: Callable[P, Awaitable[None]]) -> Loop[P]:
        return Loop(
            function=function,
            delay=delay,
            count=count,
            reconnect=reconnect,
        )

    return wrap
