from typing import Final
from asyncio import create_task
import logging

from src.core.exc.repo import RepoError
from src.schemas.link import Link
from src.service.abstraction import ILinkRepo, ICacheRepo
from src.utils.catch import handle_timeout_and_error


WAIT_REPO_TIME: Final = 2


class LinkService:
    __slots__ = ('link_repo', 'cache_repo')

    def __init__(self, link_repo: ILinkRepo, cache_repo: ICacheRepo) -> None:
        self.link_repo: ILinkRepo = link_repo
        self.cache_repo: ICacheRepo = cache_repo

    @handle_timeout_and_error(error_type=RepoError, message='cant add add links in database')
    async def add_links(self, links: tuple[Link, ...]) -> None:
        await self.link_repo.add_links(tuple(
            {
                'link': link.link,
                'status': link.status,
                'views': 1
            }

            for link in links
        ))

    @handle_timeout_and_error(error_type=RepoError, message='cant find most popular links in database')
    async def get_most_popular_links(self, limit: int) -> tuple[Link, ...]:
        links_from_cache = await self.cache_repo.get_links()
        if links_from_cache is not None and len(links_from_cache) >= limit:
            logging.info('link service: get links from cache')
            return links_from_cache[:limit]

        links_from_db = await self.link_repo.get_most_popular_links(limit)
        links = tuple(
            Link(
                link=link.link,
                status=link.status,
                views=link.views
            )
            for link in links_from_db)

        create_task(self.cache_repo.save_links(links))
        logging.info('link service: get links from database')
        return links
