from src.core.logger.logger import setup_logger
from src.core.migrations.cassandra import MigrationMethod, apply_migrations
from src.core.settings.settings import settings
from src.database.cassandra import connect_to_cassandra
from src.dependencies.service import get_link_service, init_link_service
from src.fabric.repo import LinkRepoFabric
from src.fabric.service import LinkServiceFabric


async def init_app() -> None:
    setup_logger()

    cluster, session = await connect_to_cassandra(settings)
    await apply_migrations(session, MigrationMethod.UP)

    repo = await LinkRepoFabric.new_repo(cluster, session)
    service = await LinkServiceFabric.new_service(repo)

    await init_link_service(service)


async def close_app() -> None:
    service = await get_link_service()
    await service.close()
