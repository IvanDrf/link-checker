import logging
from asyncio import Semaphore, create_task, gather
from typing import Final

from async_cassandra import AsyncCassandraSession, AsyncCluster
from async_cassandra.exceptions import AsyncCassandraError

from src.core.exc.repo import RepoError
from src.schemas.link import Link


MAX_CONCURRENCY: Final = 20


class LinkRepo:
    def __init__(self, cluster: AsyncCluster, session: AsyncCassandraSession) -> None:
        self.cluster: AsyncCluster = cluster
        self.session: AsyncCassandraSession = session

    async def close(self) -> None:
        await self.session.close()
        await self.cluster.shutdown()

    async def add_links(self, links: tuple[Link, ...]) -> None:
        try:
            stmt = await self.session.prepare('UPDATE links SET count = count + 1 WHERE link = ?')

            semaphore = Semaphore(MAX_CONCURRENCY)

            tasks = tuple(create_task(self._add_link(
                semaphore, stmt, link)) for link in links)

            await gather(*tasks, return_exceptions=True)

        except AsyncCassandraError as e:
            logging.error(f'Link repo error: {e.__str__()}')
            raise RepoError('cant save links in database')

    async def _add_link(self, semaphore: Semaphore, stmt, link: Link):
        async with semaphore:
            await self.session.execute(query=stmt, parameters=(link.link,))

    async def get_links(self, limit: int) -> tuple[Link, ...]:
        try:
            stmt = await self.session.prepare('SELECT link, count FROM links LIMIT ?')
            rows = await self.session.execute(query=stmt, parameters=(limit,))

            return tuple([Link(link=row[0], count=row[1]) async for row in rows])

        except AsyncCassandraError as e:
            logging.error(f'Link repo error: {e.__str__()}')
            raise RepoError('cant get links from database')

    async def get_most_popular_links(self, limit: int) -> tuple[Link, ...]:
        try:
            stmt = await self.session.prepare('SELECT link, count FROM links ORDER BY count ASC LIMIT ?')
            rows = await self.session.execute(query=stmt, parameters=(limit,))

            return tuple([Link(link=row[0], count=row[1]) async for row in rows])

        except AsyncCassandraError as e:
            logging.error(f'Link repo error: {e.__str__()}')
            raise RepoError('cant get most popular links from database')
