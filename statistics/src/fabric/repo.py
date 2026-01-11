from src.core.settings.postgresql import DatabaseSettings
from src.core.settings.redis import RedisSettings
from src.database.postgresql import connect_to_database
from src.database.redis import connect_to_redis
from src.repo.cache import CacheRepo
from src.repo.links import LinkRepo
from src.service.abstraction import ICacheRepo, ILinkRepo


class LinkRepoFabric:
    @staticmethod
    async def new_link_repo(settings: DatabaseSettings) -> ILinkRepo:
        session_maker, _ = await connect_to_database(settings)
        return LinkRepo(session_maker)


class CacheRepoFabric:
    @staticmethod
    async def new_cache_repo(settings: RedisSettings) -> ICacheRepo:
        redis = await connect_to_redis(settings)
        return CacheRepo(redis)
