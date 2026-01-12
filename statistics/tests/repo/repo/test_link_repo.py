from asyncio import gather

from pytest import fail, mark
from sqlalchemy import select

from src.models.link import LinkOrm
from src.repo.links import LinkRepo
from src.schemas.link import Link
from src.service.links import convert_links_for_db
from tests.utils import is_links_are_same


@mark.asyncio
async def test_add_links(link_repo: LinkRepo, links_for_db, links) -> None:
    try:
        await link_repo.add_links(links_for_db)
    except Exception as e:
        fail(f'unexpected error: {e.__str__()}')

    async with link_repo.session_maker() as session:
        res = await session.scalars(select(LinkOrm))

        links_from_db = tuple(res.fetchall())

        assert is_links_are_same(links_from_db, links) is True


@mark.asyncio
async def test_get_popular_links(link_repo: LinkRepo, links, limits, repeated) -> None:
    await insert_links(link_repo, links, repeated)

    for limit in limits:
        links_from_db = await link_repo.get_most_popular_links(limit)

        assert len(links_from_db) == limit
        # assert is_links_are_same(links_from_db, links) is True


async def insert_links(link_repo: LinkRepo, links: tuple[Link, ...], repeated: int) -> None:
    links_for_db = convert_links_for_db(links)

    results = await gather(*(link_repo.add_links(links_for_db) for _ in range(repeated)), return_exceptions=True)
    for res in results:
        if isinstance(res, BaseException):
            fail(f'unexpected error: {res.__str__()}')
