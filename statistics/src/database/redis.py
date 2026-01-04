from redis.asyncio import Redis

from src.core.settings.redis import RedisSettings
from src.core.exc.internal import InternalError


async def connect_to_redis(settings: RedisSettings) -> Redis:
    redis = Redis(
        host=settings.host,
        port=settings.port,
        password=settings.password,
        db=settings.database,

    )

    if await redis.ping():  # type: ignore
        return redis

    raise InternalError('cant connect to redis')
