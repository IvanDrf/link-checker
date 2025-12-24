from pytest import mark

from app.repo.repo import Repo
from app.models.user import User

from typing import Final, Optional

USER_ID: Final = 123456789
INVALID_USER_ID: Final = -1


@mark.asyncio
async def test_add_user(repo: Repo) -> None:
    user_id: Optional[int] = await repo.add_user(USER_ID)
    print(user_id)
    assert user_id is not None
    assert user_id == USER_ID


@mark.asyncio
async def test_find_user(repo: Repo) -> None:
    user: Optional[User] = await repo.find_user(USER_ID)

    assert user is not None
    assert user.user_id == USER_ID
    assert user.links_amount == 0

    user = await repo.find_user(INVALID_USER_ID)
    assert user is None


@mark.asyncio
async def test_add_links_amount(repo: Repo) -> None:
    LINKS_AMOUNT: Final = 1

    user: Optional[User] = await repo.add_links_amount(USER_ID, LINKS_AMOUNT)

    assert user is not None
    assert user.user_id == USER_ID
    assert user.links_amount == LINKS_AMOUNT

    user = await repo.add_links_amount(INVALID_USER_ID, LINKS_AMOUNT)
    assert user is None


@mark.asyncio
async def test_reduce_links_amount(repo: Repo) -> None:
    LINKS_AMOUNT: Final = 1

    user: Optional[User] = await repo.reduce_links_amount(USER_ID, LINKS_AMOUNT)

    assert user is not None
    assert user.user_id == USER_ID
    assert user.links_amount == 0  # was 1 in previous test
