from pytest import mark, fail

from typing import Final

from app.repo.redis import RedisRepo
from app.schemas.message import LinkMessage
from app.exc.internal import InternalError


@mark.asyncio
async def test_save_links(redis_repo: RedisRepo, links: LinkMessage) -> None:
    try:
        await redis_repo.save_links(links.user_id, links)
    except InternalError as e:
        fail(f'got unexpected error -> {e.__str__()}')


@mark.asyncio
async def test_get_links(redis_repo: RedisRepo, links: LinkMessage) -> None:
    try:
        await redis_repo.save_links(links.user_id, links)
    except InternalError as e:
        fail(f'got unexpected error -> {e.__str__()}')

    try:
        links_from_redis = await redis_repo.get_links(links.user_id)
        assert links_from_redis == links.links

    except InternalError as e:
        fail(f'got unexpected error -> {e.__str__()}')


@mark.asyncio
async def test_bad_get_links(redis_repo: RedisRepo) -> None:
    INVALID_USER_ID: Final = -1

    try:
        links = await redis_repo.get_links(INVALID_USER_ID)
        assert len(links) == 0

    except InternalError:
        fail('should not be exceptions')
