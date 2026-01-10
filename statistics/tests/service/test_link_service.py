from asyncio import sleep

from pytest import fail, mark

from src.schemas.link import Link
from src.service.links import LinkService


@mark.asyncio
async def test_add_links(link_service: LinkService, links: tuple[Link, ...]) -> None:
    try:
        await link_service.add_links(links)
        await link_service.add_links(tuple(links[:len(links) // 2]))
    except Exception as e:
        fail(f'unexpected exception: {e.__str__()}')


@mark.asyncio
async def test_get_most_popular_links(link_service: LinkService, limits: tuple[int, ...]) -> None:
    links_from_repo = []

    async def get_links(output: list[Link]) -> None:
        for limit in limits:
            links = await link_service.get_most_popular_links(limit)

            assert len(links) <= limit
            assert all(links[i].views >= links[i].views
                       for i in range(len(links) - 1))

            output.append(links)

    await get_links(links_from_repo)

    # clear repo, for testing if values are gotten from cache
    clear_links: tuple[Link, ...] = Link(link='', status=False, views=0),
    await link_service.add_links(clear_links)
    await sleep(0.5)

    links_from_cache = []
    await get_links(links_from_cache)

    assert len(links_from_repo) == len(links_from_cache)
