from src.core.logger.logger import setup_logger
from src.dependencies.service import init_link_service
from src.fabric.repo import LinkRepoFabric
from src.fabric.service import LinkServiceFabric


async def init_app() -> None:
    setup_logger()

    repo = await LinkRepoFabric.new_repo()
    service = await LinkServiceFabric.new_service(repo)

    await init_link_service(service)
