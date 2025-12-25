from typing import Optional

from pytest import mark

from app.models.user import User
from app.repo.repo import Repo


@mark.asyncio
async def test_add_user(repo: Repo, USER_ID: int) -> None:
    user_id: Optional[int] = await repo.add_user(USER_ID)

    assert user_id is not None
    assert user_id == USER_ID


@mark.asyncio
async def test_find_user(repo: Repo, USER_ID: int, INVALID_USER_ID: int) -> None:
    await repo.add_user(USER_ID)

    user: Optional[User] = await repo.find_user(USER_ID)

    assert user is not None
    assert user.user_id == USER_ID
    assert user.links_amount == 0

    user = await repo.find_user(INVALID_USER_ID)
    assert user is None
