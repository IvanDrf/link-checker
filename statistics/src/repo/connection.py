import logging
from functools import wraps
from typing import Any, Callable

from sqlalchemy.exc import SQLAlchemyError

from src.database.postgresql import session_maker


def connection(error_type: type[Exception], error_message: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with session_maker() as session:
                try:
                    res = await func(session, *args, **kwargs)

                    await session.commit()
                    return res
                except SQLAlchemyError as e:
                    await session.rollback()

                    logging.error(f'SQL error: {e.__str__()}')
                    raise error_type(error_message)

        return wrapper

    return decorator
