from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy import insert, delete, select
from typing import Optional

from app.models.link import Link
from app.repo.connection import connection


class LinkRepo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False)

    @connection
    async def _save_link(self, session: AsyncSession, link: str, user_id: int) -> Optional[int]:
        stmt = insert(Link).values({"user_id": user_id, "link": link})

        await session.execute(stmt)
        return user_id

    @connection
    async def _delete_link(self, session: AsyncSession, link: str, user_id: int) -> int:
        stmt = delete(Link).where(Link.user_id == user_id,
                                  Link.link == link).returning(Link.id)

        res = await session.execute(stmt)
        return len(res.scalars().all())

    @connection
    async def find_links(self, session: AsyncSession, user_id: int) -> Optional[list]:
        stmt = select(Link).where(Link.user_id == user_id)

        res = await session.scalars(stmt)
        links = res.fetchall()

        return list(links) if links else None
