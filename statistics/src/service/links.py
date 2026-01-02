from typing import Final

from src.core.exc.repo import RepoError
from src.schemas.link import Link
from src.service.abstraction import ILinkRepo
from src.service.catch import handle_timeout_and_error


WAIT_REPO_TIME: Final = 2


class LinkService:
    def __init__(self, repo: ILinkRepo) -> None:
        self.link_repo: ILinkRepo = repo

    @handle_timeout_and_error(error_type=RepoError, message='cant add add links in database')
    async def add_links(self, links: tuple[Link, ...]) -> None:
        await self.link_repo.add_links(links)

    @handle_timeout_and_error(error_type=RepoError, message='cant find most popular links in database')
    async def get_most_popular_links(self, limit: int) -> tuple[Link, ...]:
        links = await self.link_repo.get_most_popular_links(limit)
        return links
