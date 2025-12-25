from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.exc.internal import InternalError
from app.repo.connection import connection
from app.repo.link import LinkRepo
from app.repo.user import UserRepo


class Repo(UserRepo, LinkRepo):
    def __init__(self, engine: AsyncEngine) -> None:
        UserRepo.__init__(self, engine)
        LinkRepo.__init__(self, engine)

    @connection
    async def save_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        res = await self._save_link(session, link, user_id)
        if res is None:
            raise InternalError('cant save link in database')

        res = await self._add_links_amount(session, user_id, 1)
        if res is None:
            raise InternalError('cant change links amount in database')

        return user_id

    @connection
    async def delete_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        res = await self._delete_link(session, link, user_id)
        if res == 0:
            raise InternalError('cant delete link in databsae')

        res = await self._reduce_links_amount(session, user_id, 1)
        if res is None:
            raise InternalError('cant reduce links amount in database')

        return user_id
