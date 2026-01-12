from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from alembic.command import upgrade, downgrade
from alembic.config import Config
from src.core.settings.settings import settings
from src.database.postgresql import connect_to_database
from src.repo.links import LinkRepo
from src.schemas.link import Link
from src.models.link import LinkOrm
from src.service.links import convert_links_for_db


@fixture(scope='package', autouse=True)
def apply_migrations():
    alembic_config = Config('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', settings.database.dsn)

    upgrade(alembic_config, 'head')

    yield

    downgrade(alembic_config, 'base')


@async_fixture(scope='package')
async def link_repo() -> LinkRepo:
    session_maker, _ = await connect_to_database(settings.database)

    return LinkRepo(session_maker)


@fixture(scope='function')
def links_for_db(links: tuple[Link, ...]) -> tuple[dict[str, str | int | bool], ...]:
    return convert_links_for_db(links)


@fixture(scope='function')
def links_orm(links: tuple[Link, ...]) -> tuple[LinkOrm, ...]:
    return tuple(
        LinkOrm(link=link.link, status=link.status, views=link.views)
        for link in links
    )
