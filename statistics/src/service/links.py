import logging
from asyncio import timeout
from typing import Final

from src.core.exc.internal import InternalError
from src.core.exc.repo import RepoError
from src.schemas.link import Link
from src.service.abstraction import ILinkRepo


WAIT_REPO_TIME: Final = 2


class LinkService:
    def __init__(self, repo: ILinkRepo) -> None:
        self.link_repo: ILinkRepo = repo

    async def add_links(self, links: tuple[Link, ...]) -> None:
        try:
            async with timeout(WAIT_REPO_TIME):
                await self.link_repo.add_links(links)
        except TimeoutError as e:
            logging.error(f'REPO error timeout: {e.__str__()}')
            raise InternalError('timeout for saving links in database')

        except RepoError as e:
            logging.error(e.__str__())
            raise InternalError('cant add links to database')

    async def close(self) -> None:
        await self.link_repo.close()
