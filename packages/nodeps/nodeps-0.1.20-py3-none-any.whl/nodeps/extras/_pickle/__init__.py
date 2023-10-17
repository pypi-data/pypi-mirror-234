"""NoDeps Extras Pickle Module."""
__all__ = (
    "cache",
)

import functools
import inspect
from collections.abc import Callable, Coroutine
from typing import Any, Generic, TypeVar

try:
    # nodeps[pickle] extras
    import jsonpickle  # type: ignore[attr-defined]
    import structlog  # type: ignore[attr-defined]
    import structlog.stdlib  # type: ignore[attr-defined]
except ModuleNotFoundError:
    jsonpickle = None
    structlog = None

_T = TypeVar("_T")


class _CacheWrapper(Generic[_T]):
    __wrapped__: Callable[..., _T]

    def __call__(self, *args: Any, **kwargs: Any) -> _T | Coroutine[Any, Any, _T]:
        ...


def cache(
    func: Callable[..., _T | Coroutine[Any, Any, _T]] = ...
) -> Callable[[Callable[..., _T]], _CacheWrapper[_T]] | _T | Coroutine[Any, Any, _T] | Any:
    """Caches previous calls to the function if object can be encoded.

    Examples:
        >>> import asyncio
        >>> from typing import cast
        >>> from typing import Coroutine
        >>> from environs import Env as Environs
        >>> from collections import namedtuple
        >>> from nodeps.extras._pickle import cache
        >>>
        >>> @cache
        ... def test(a):
        ...     print(True)
        ...     return a
        >>>
        >>> @cache
        ... async def test_async(a):
        ...     print(True)
        ...     return a
        >>>
        >>> test({})
        True
        {}
        >>> test({})
        {}
        >>> asyncio.run(cast(Coroutine, test_async({})))
        True
        {}
        >>> asyncio.run(cast(Coroutine, test_async({})))
        {}
        >>> test(Environs())
        True
        <Env {}>
        >>> test(Environs())
        <Env {}>
        >>> asyncio.run(cast(Coroutine, test_async(Environs())))
        True
        <Env {}>
        >>> asyncio.run(cast(Coroutine, test_async(Environs())))
        <Env {}>
        >>>
        >>> @cache
        ... class Test:
        ...     def __init__(self, a):
        ...         print(True)
        ...         self.a = a
        ...
        ...     @property
        ...     @cache
        ...     def prop(self):
        ...         print(True)
        ...         return self
        >>>
        >>> Test({})  # doctest: +ELLIPSIS
        True
        <....Test object at 0x...>
        >>> Test({})  # doctest: +ELLIPSIS
        <....Test object at 0x...>
        >>> Test({}).a
        {}
        >>> Test(Environs()).a
        True
        <Env {}>
        >>> Test(Environs()).prop  # doctest: +ELLIPSIS
        True
        <....Test object at 0x...>
        >>> Test(Environs()).prop  # doctest: +ELLIPSIS
        <....Test object at 0x...>
        >>>
        >>> Test = namedtuple('Test', 'a')
        >>> @cache
        ... class TestNamed(Test):
        ...     __slots__ = ()
        ...     def __new__(cls, *args, **kwargs):
        ...         print(True)
        ...         return super().__new__(cls, *args, **kwargs)
        >>>
        >>> TestNamed({})
        True
        TestNamed(a={})
        >>> TestNamed({})
        TestNamed(a={})
        >>> @cache
        ... class TestNamed(Test):
        ...     __slots__ = ()
        ...     def __new__(cls, *args, **kwargs): return super().__new__(cls, *args, **kwargs)
        ...     def __init__(self): super().__init__()
        >>> TestNamed({}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError: __init__() takes 1 positional argument but 2 were given
    """
    if jsonpickle is None or structlog is None:
        msg = "structlog and/or jsonpickle are not installed: installed with 'pip install nodeps[cache]'"
        raise ImportError(msg)
    memo = {}
    log = structlog.get_logger()
    coro = inspect.iscoroutinefunction(func)
    if coro:

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            """Async Cache Wrapper."""
            key = None
            save = True
            try:
                key = jsonpickle.encode((args, kwargs))
                if key in memo:
                    return memo[key]
            except Exception as exception:  # noqa: BLE001
                log.warning("Not cached", func=func, args=args, kwargs=kwargs, exception=exception)
                save = False
            value = await func(*args, **kwargs)
            if key and save:
                memo[key] = value
            return value
    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Cache Wrapper."""
            key = None
            save = True
            try:
                key = jsonpickle.encode((args, kwargs))
                if key in memo:
                    return memo[key]
            except Exception as exception:  # noqa: BLE001
                log.warning("Not cached", func=func, args=args, kwargs=kwargs, exception=exception)
                save = False
            value = func(*args, **kwargs)
            if key and save:
                memo[key] = value
            return value
    return wrapper
