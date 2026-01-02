from typing import Final
import logging

from sqlalchemy import select, Select
from sqlalchemy.dialects.postgresql import insert, Insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.core.exc.repo import RepoError
from src.database.postgresql import session_maker
from src.models.link import LinkOrm

MAX_CONCURRENCY: Final = 20


class LinkRepo:
    async def add_links(self, links: tuple[dict[str, str | bool | int], ...]) -> None:
        stmt = insert(LinkOrm).values(links)
        conflict_stmt = stmt.on_conflict_do_update(
            index_elements=['link'],
            set_={
                'status': stmt.excluded.status,
                'views': LinkOrm.views + 1
            }
        )

        async with session_maker() as session, session.begin():
            return await self._add_links(session, conflict_stmt)

    async def _add_links(self, session: AsyncSession, stmt: Insert) -> None:
        try:
            await session.execute(stmt)
            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()

            logging.error(f'SQLAlchemy error: {e.__str__()}')
            raise RepoError('cant add links in database')

    async def get_most_popular_links(self, limit: int) -> tuple[LinkOrm, ...]:
        stmt = select(LinkOrm).order_by(LinkOrm.views).limit(limit)

        async with session_maker() as session:
            return await self._get_most_popular_links(session, stmt)

    async def _get_most_popular_links(self, session: AsyncSession, stmt: Select[tuple[LinkOrm]]) -> tuple[LinkOrm, ...]:
        try:
            res = await session.scalars(stmt)
            links = res.fetchall()

            return tuple(links)

        except SQLAlchemyError as e:
            logging.error(f'SQLAlchemy error: {e.__str__()}')
            raise RepoError('cant find most popular links in database')
