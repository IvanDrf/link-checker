from json import dumps
from typing import Any, AsyncGenerator

from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from pytest_redis.factories import redis_proc
from redis.asyncio import Redis

from src.repo.cache import CacheRepo
from src.schemas.link import Link


@async_fixture(scope='function')
async def redis(redis_proc) -> AsyncGenerator[Redis, Any]:
    redis = Redis(
        host=redis_proc.host,
        port=redis_proc.port,
        password=redis_proc.password
    )

    yield redis
    await redis.aclose()


@async_fixture(scope='function')
async def cache_repo(redis) -> CacheRepo:
    cache = CacheRepo(redis)

    return cache


@fixture(scope='package')
def links_json(links: tuple[Link, ...]) -> str:
    return dumps([link.model_dump() for link in links])
