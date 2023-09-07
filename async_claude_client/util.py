import asyncio
import functools
from contextvars import copy_context
from functools import wraps, partial
from typing import (
    TypeVar,
    Callable,
    Coroutine,
)

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def retry(tries, error_message):
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            error = None
            for _ in range(tries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error = e
            raise Exception(f"{error_message}: {error}")

        async def async_wrapper(*args, **kwargs):
            error = None
            for _ in range(tries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error = e
            raise Exception(f"{error_message}: {error}")

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        context = copy_context()
        result = await loop.run_in_executor(None, partial(context.run, pfunc))
        return result

    return _wrapper
