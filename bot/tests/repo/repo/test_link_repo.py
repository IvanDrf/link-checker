from typing import Final, Optional

from pytest import mark

from app.models.link import Link
from app.models.user import User
from app.repo.repo import Repo


LINK: Final = 'google.com'
LINKS: Final = ('google.com', 'vk.com', 'habr.com', 'github.com')
INVALID_LINK: Final = '123'


@mark.asyncio
async def test_save_link(repo: Repo, USER_ID: int, INVALID_USER_ID: int) -> None:
    await repo.add_user(USER_ID)

    user_id: Optional[int] = await repo.save_link(LINK, USER_ID)

    assert user_id is not None
    assert user_id == USER_ID

    user: Optional[User] = await repo.find_user(USER_ID)

    assert user is not None
    assert user.user_id == USER_ID
    assert user.links_amount == 1

    user_id = await repo.save_link(INVALID_USER_ID)

    assert user_id is None


@mark.asyncio
async def test_delete_link(repo: Repo, USER_ID: int, INVALID_USER_ID: int) -> None:
    await repo.add_user(USER_ID)
    await repo.save_link(LINK, USER_ID)

    user_id: Optional[int] = await repo.delete_link(LINK, USER_ID)

    assert user_id is not None
    assert user_id == USER_ID

    user_id = await repo.delete_link(LINK, INVALID_USER_ID)
    assert user_id is None

    user_id = await repo.delete_link(INVALID_LINK, USER_ID)
    assert user_id is None

    user_id = await repo.delete_link(INVALID_LINK, INVALID_USER_ID)
    assert user_id is None


@mark.asyncio
async def test_find_links(repo: Repo, USER_ID: int, INVALID_USER_ID: int) -> None:
    await repo.add_user(USER_ID)

    links: Optional[tuple[Link, ...]] = await repo.find_links(USER_ID)
    assert links is None

    # add some links for test
    for link in LINKS:
        user_id: Optional[int] = await repo.save_link(link, USER_ID)
        assert user_id is not None
        assert user_id == USER_ID

    links = await repo.find_links(USER_ID)

    assert links is not None
    assert len(links) == len(LINKS)

    for i, link in enumerate(LINKS):
        assert links[i].link == link

    links = await repo.find_links(INVALID_USER_ID)
    assert links is None
