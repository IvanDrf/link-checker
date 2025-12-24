import logging
from functools import wraps
from typing import Any, Callable, Optional, Protocol

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class _AsyncSessioner(Protocol):
    def async_session(self) -> AsyncSession:
        ...


def connection(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(self: _AsyncSessioner, *args, **kwargs) -> Optional[Any]:
        async with self.async_session() as session:
            try:
                result = await func(self, session, *args, **kwargs)

                await session.commit()
                return result
            except (SQLAlchemyError, Exception) as e:
                logging.error(f'{func.__name__}-> {e}')

                await session.rollback()
                return None

    return wrapper
