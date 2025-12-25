from redis.asyncio import Redis

from app.commands.abstraction.repo import IRedisRepo
from app.config.config import Config
from app.database.redis import connect_to_redis
from app.repo.redis import RedisRepo


class RedisRepoFabric:
    @staticmethod
    async def new_redis_repo(cfg: Config) -> IRedisRepo:
        redis: Redis = await connect_to_redis(cfg)

        return RedisRepo(redis)
