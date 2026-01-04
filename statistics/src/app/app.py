from src.core.logger.logger import setup_logger
from src.core.settings.settings import settings

from src.dependencies.service import init_link_service
from src.fabric.repo import LinkRepoFabric, CacheRepoFabric
from src.fabric.service import LinkServiceFabric


async def init_app() -> None:
    setup_logger()

    link_repo = await LinkRepoFabric.new_link_repo(settings.database)
    cache_repo = await CacheRepoFabric.new_cache_repo(settings.cache)
    service = LinkServiceFabric.new_service(link_repo, cache_repo)

    init_link_service(service)
