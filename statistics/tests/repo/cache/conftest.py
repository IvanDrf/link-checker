from typing import AsyncGenerator, Any
from json import dumps

from redis.asyncio import Redis

from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from pytest_redis.factories import redis_proc

from src.service.abstraction import ICacheRepo
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
async def cache_repo(redis) -> ICacheRepo:
    cache = CacheRepo(redis)

    return cache


@fixture(scope='package')
def links() -> tuple[Link, ...]:
    return (
        Link(link='google.com', status=True, views=10),
        Link(link='vk.com', status=True, views=1),
        Link(link='ya.ru', status=True, views=2),
        Link(link='habr.com', status=True, views=3),
        Link(link='test.com', status=True, views=6)
    )


@fixture(scope='package')
def links_json(links) -> str:
    return dumps([link.model_dump() for link in links])
