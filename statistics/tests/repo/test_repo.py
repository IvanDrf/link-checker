from pytest import fail, mark

from src.core.exc.repo import RepoError
from src.repo.links import LinkRepo
from src.schemas.link import Link


add_links_expected = (
    Link(link='google.com', view=2),
    Link(link='vk.com', view=1),
    Link(link='ya.ru', view=1),
    Link(link='habr.com', view=1),
)


@mark.asyncio
async def test_add_links(link_repo: LinkRepo, links: tuple[Link, ...]) -> None:
    try:
        await link_repo.add_links(links)
    except RepoError as e:
        fail(f'Unexpected error: {e.__str__()}')

    try:
        links_from_db = await link_repo.get_links(limit=len(links))
        assert links_from_db == add_links_expected

    except RepoError as e:
        fail(f'Unexpected error: {e.__str__()}')
