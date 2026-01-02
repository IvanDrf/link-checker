from typing import Final

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exc.repo import RepoError
from src.models.link import Link
from src.repo.connection import connection


MAX_CONCURRENCY: Final = 20


class LinkRepo:
    @connection(error_type=RepoError, error_message='cant save links in database')
    async def add_links(self, session: AsyncSession, links: tuple[Link, ...]) -> None:
        stmt = insert(Link).values(links)
        await session.execute(stmt)

    @connection(error_type=RepoError, error_message='cant find most popular links in database')
    async def get_most_popular_links(self, session: AsyncSession, limit: int) -> tuple[Link, ...]:
        stmt = select(Link).order_by(Link.views).limit(limit)

        res = await session.scalars(stmt)
        links = res.fetchall()

        return tuple(link for link in links)
