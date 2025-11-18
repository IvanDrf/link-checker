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
    async def save_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        self.add_user
        res = await self._save_link(link, user_id)
        if res is None:
            return None

        res = await self.add_links_amount(user_id, 1)
        if res is None:
            return None

        return user_id

    @connection
    async def delete_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        res = await self._delete_link(link, user_id)
        if res == 0:
            return None

        res = await self.reduce_links_amount(user_id, 1)
        if res is None:
            return None

        return user_id
