from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from typing import Optional

from app.repo.user import UserRepo
from app.repo.link import LinkRepo
from app.repo.connection import connection


class Repo(UserRepo, LinkRepo):
    def __init__(self, engine: AsyncEngine) -> None:
        UserRepo.__init__(self, engine)
        LinkRepo.__init__(self, engine)

    @connection
    async def add_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        res = await self._add_link(link, user_id)
        if res is None:
            return None

        res = await self.add_links_amount(user_id, 1)
        if res is None:
            return None

        return user_id

    @connection
    async def remove_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        res = await self._remove_link(link, user_id)
        if res is None:
            return None

        res = await self.reduce_links_amount(user_id, 1)
        if res is None:
            return None

        return user_id
