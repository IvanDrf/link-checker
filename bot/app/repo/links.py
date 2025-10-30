from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy import insert
from typing import Optional

from app.models.link import Link


class LinkRepo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            engine, class_=AsyncSession)

    async def add_link(self, link: str, user_id: int) -> Optional[Link]:
        async with self.async_session() as session:
            pass
