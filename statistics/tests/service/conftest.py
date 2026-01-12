from asyncio import sleep
from typing import Optional

from pytest import fixture

from src.models.link import LinkOrm
from src.repo.cache import LINKS_KEY, format_links_to_json
from src.schemas.link import Link, Links
from src.service.links import LinkService


class LinkRepoTest:
    def __init__(self) -> None:
        self.links: dict[str, LinkOrm] = {}

    async def add_links(self, links: tuple[dict[str, str | int | bool], ...]) -> None:
        if len(links) == 1:  # clear repo, for testing if values are gotten from cache
            self.links = {}
            return

        for link in links:
            await sleep(0)
            if link['link'] not in self.links:
                self.links[link['link']] = LinkOrm(  # type: ignore
                    link=link['link'],
                    status=link['status'],
                    views=link['views']
                )
            else:
                self.links[link['link']].views += 1  # type: ignore
                # format: ignore
                # type: ignore
                self.links[link['link']].status = link['status']  # type: ignore # noqa

    async def get_most_popular_links(self, limit: int) -> tuple[LinkOrm, ...]:
        return tuple(sorted(self.links.values(), key=lambda arg: arg.views, reverse=True)[:limit])


class CacheRepoTest:
    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    async def close(self) -> None:
        pass

    async def save_links(self, links: tuple[Link, ...]) -> None:
        if len(links) == 1:
            return

        links_json = format_links_to_json(links)

        self.cache[LINKS_KEY] = links_json

    async def get_links(self) -> Optional[tuple[Link, ...]]:
        try:
            links_json = self.cache[LINKS_KEY]
        except KeyError:
            return None

        return Links.validate_json(links_json)


@fixture(scope='package')
def link_service() -> LinkService:
    return LinkService(link_repo=LinkRepoTest(), cache_repo=CacheRepoTest())
