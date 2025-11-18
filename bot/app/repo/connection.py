from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from typing import Callable, Any, Optional
from functools import wraps
import logging


def connection(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> Optional[Any]:
        session: AsyncSession

        async with self.async_session() as session:
            try:
                result = await func(self, session, *args, **kwargs)

                await session.commit()
                return result
            except SQLAlchemyError as e:
                logging.error(f'{func.__name__}-> {e}')

                await session.rollback()
                return None
            except Exception as e:
                logging.error(f'{func.__name__}-> {e}')

                await session.rollback()
                return None

    return wrapper
