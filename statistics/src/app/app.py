from src.core.logger.logger import setup_logger
from src.core.settings.settings import settings
from src.dependencies.service import init_link_service
from src.fabric.repo import LinkRepoFabric
from src.fabric.service import LinkServiceFabric


async def init_app() -> None:
    setup_logger()

    repo = await LinkRepoFabric.new_repo(settings.database)
    service = LinkServiceFabric.new_service(repo)

    init_link_service(service)
