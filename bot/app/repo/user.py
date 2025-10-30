from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select
from typing import Optional
import logging

from app.models.user import User


class UserRepo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            engine, class_=AsyncSession)

    async def add_user(self, user_id: int) -> Optional[int]:
        async with self.async_session() as session:
            try:
                stmt = insert(User).values(
                    {"user_id": user_id, "links:amount": 0})
                await session.execute(stmt)

                await session.commit()
                return user_id

            except SQLAlchemyError as e:
                logging.info(f'add_user -> {e}')

                return None

    async def add_links_amount(self, user_id: int, links_amount: int) -> Optional[User]:
        if links_amount <= 0:
            return None

        await self.__change_links_amount(user_id, links_amount)

    async def reduce_links_amount(self, user_id: int, links_amount: int) -> Optional[User]:
        if links_amount <= 0:
            return None

        links_amount *= -1

        await self.__change_links_amount(user_id, links_amount)

    async def __change_links_amount(self, user_id: int, links_amount: int) -> Optional[User]:
        async with self.async_session() as session:
            try:
                user = await session.scalar(select(User).filter_by(user_id=user_id))
                if user is None:
                    logging.info(
                        f'add_links_amount -> cant find user with this id {user_id}')

                    return None

                user.links_amount += links_amount

                await session.commit()
                return user

            except SQLAlchemyError as e:
                logging.error(f'change_links_amount-> {e}')

                await session.rollback()
                return None
