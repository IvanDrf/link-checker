from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from redis.asyncio import Redis

from app.repo.redis import RedisRepo
from app.schemas.message import LinkMessage, LinkStatus


@async_fixture
async def redis(redis_proc):
    client = Redis(host=redis_proc.host, port=redis_proc.port)

    yield client
    await client.aclose()


@fixture
def redis_repo(redis: Redis) -> RedisRepo:
    return RedisRepo(redis)


@fixture(scope='package')
def links() -> LinkMessage:
    return LinkMessage(
        user_id=1234567,
        chat_id=456789,
        links=(
            LinkStatus(link='google.com', status=True),
            LinkStatus(link='vk.com', status=True),
            LinkStatus(link='habr.com', status=True),
            LinkStatus(link='badlink', status=False),
            LinkStatus(link='123.fm', status=False),
        )
    )
