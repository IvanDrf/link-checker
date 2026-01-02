import logging
from asyncio import timeout
from functools import wraps
from typing import Any, Callable, Final

from src.core.exc.internal import InternalError


WAIT_REPO_TIME: Final = 2


def handle_timeout_and_error(error_type: type[Exception], message: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                async with timeout(WAIT_REPO_TIME):
                    res = await func(*args, **kwargs)
                    return res
            except TimeoutError as e:
                logging.error(f'REPO error timeout: {e.__str__()}')
                raise InternalError(f'timeout for {message}')

            except error_type as e:
                logging.error(e.__str__())
                raise InternalError(message)

        return wrapper

    return decorator
