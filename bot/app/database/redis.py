from redis.asyncio import Redis

from app.config.config import Config


async def connect_to_redis(cfg: Config) -> Redis:
    redis = Redis(
        host=cfg.redis.host,
        port=cfg.redis.port,
        password=cfg.redis.password,
        db=cfg.redis.db
    )

    return redis
