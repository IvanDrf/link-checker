from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from alembic.command import downgrade, upgrade
from alembic.config import Config
from src.core.settings.settings import settings
from src.database.postgresql import connect_to_database
from src.repo.links import LinkRepo
from src.schemas.link import Link
from src.service.links import convert_links_for_db


@fixture(scope='function', autouse=True)
def apply_migrations():
    alembic_config = Config('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', settings.database.dsn)

    upgrade(alembic_config, 'head')

    yield

    downgrade(alembic_config, 'base')


@async_fixture(scope='function')
async def link_repo() -> LinkRepo:
    session_maker, _ = await connect_to_database(settings.database)

    return LinkRepo(session_maker)


@fixture(scope='package')
def links_for_db(links: tuple[Link, ...]):
    return convert_links_for_db(links)
