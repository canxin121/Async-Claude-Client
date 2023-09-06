import asyncio
from functools import wraps


def retry(tries, error_message):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            error = None
            for _ in range(tries):
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                except Exception as e:
                    error = e
            raise Exception(f"{error_message}: {error}")

        return wrapper

    return decorator
