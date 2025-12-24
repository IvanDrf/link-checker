import logging
from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.models.user import User
from app.repo.connection import connection


class UserRepo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False)

    @connection
    async def add_user(self, session: AsyncSession, user_id: int) -> Optional[int]:
        stmt = insert(User).values({"user_id": user_id, "links_amount": 0})
        await session.execute(stmt)

        return user_id

    @connection
    async def find_user(self, session: AsyncSession, user_id: int) -> Optional[User]:
        user: Optional[User] = await session.scalar(select(User).where(User.user_id == user_id).limit(1))

        return user

    async def add_links_amount(self, user_id: int, links_amount: int) -> Optional[User]:
        if links_amount <= 0:
            logging.info(
                f'add_links_amount -> invalid links amount {links_amount}')
            return None

        return await self._change_links_amount(user_id, links_amount)

    async def reduce_links_amount(self, user_id: int, links_amount: int) -> Optional[User]:
        if links_amount <= 0:
            logging.info(
                f'reduce_links_amount -> invalid links amount {links_amount}')
            return None

        links_amount *= -1

        return await self._change_links_amount(user_id, links_amount)

    @connection
    async def _change_links_amount(self, session: AsyncSession, user_id: int, links_amount: int) -> Optional[User]:
        user: Optional[User] = await session.scalar(select(User).filter_by(user_id=user_id))
        if user is None:
            logging.info(
                f'add_links_amount -> cant find user with this id {user_id}')
            return None

        user.links_amount += links_amount

        return user
