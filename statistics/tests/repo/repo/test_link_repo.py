from pytest import mark, fail
from sqlalchemy import select

from src.repo.links import LinkRepo
from src.models.link import LinkOrm


@mark.asyncio
async def test_add_links(link_repo: LinkRepo, links_for_db: tuple[dict[str, str | int | bool]], links_orm: tuple[LinkOrm, ...]) -> None:
    try:
        await link_repo.add_links(links_for_db)
    except Exception as e:
        fail(f'unexpected error: {e.__str__()}')

    async with link_repo.session_maker() as session:
        res = await session.scalars(select(LinkOrm))

        links = tuple(res.fetchall())

        assert links == links_orm
