import logging
from asyncio import timeout
from functools import wraps
from typing import Awaitable, Callable, Final

from src.core.exc.internal import InternalError


WAIT_REPO_TIME: Final = 2


def handle_timeout_and_error(error_type: type[Exception], message: str):
    def decorator[**P, R](func: Callable[P, Awaitable[R]]):
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            try:
                async with timeout(WAIT_REPO_TIME):
                    res = await func(*args, **kwargs)
                    return res
            except TimeoutError as e:
                logging.error(f'REPO error timeout: {e.__str__()}')
                raise InternalError(f'timeout: {message}')

            except error_type as e:
                logging.error(e.__str__())
                raise InternalError(message)

        return wrapper

    return decorator
