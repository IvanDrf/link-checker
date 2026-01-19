from pytest import fail, mark

from src.schemas.link import Link
from src.service.links import LinkService
from tests.service.utils import get_links_with_limit
from tests.utils import is_links_sorted_by_views


@mark.asyncio
async def test_add_links(link_service: LinkService, links: tuple[Link, ...]) -> None:
    try:
        await link_service.add_links(links)
        await link_service.add_links(tuple(links[:len(links) // 2]))
    except Exception as e:
        fail(f'unexpected exception: {e.__str__()}')


@mark.asyncio
async def test_get_most_popular_links(links: tuple[Link, ...], link_service: LinkService, limits: tuple[int, ...]) -> None:
    await link_service.add_links(links)

    async for links, limit in get_links_with_limit(link_service, limits):
        assert len(links) == limit
        assert is_links_sorted_by_views(links)
