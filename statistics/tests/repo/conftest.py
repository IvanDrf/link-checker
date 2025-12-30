from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from src.core.migrations.cassandra import MigrationMethod, apply_migrations
from src.core.settings.app import AppSettings
from src.core.settings.cassandra import CassandraSettings
from src.core.settings.settings import Settings
from src.database.cassandra import connect_to_cassandra
from src.repo.links import LinkRepo
from src.schemas.link import Link


@async_fixture(scope='session')
async def link_repo():
    host, port = '172.20.0.2', 9042

    cluster, session = await connect_to_cassandra(settings=Settings(
        app=AppSettings(host='localhost', port=8000, logger_level='debug'),
        cassandra=CassandraSettings(host=host, port=port, key_space='stats'))
    )

    repo = LinkRepo(cluster, session)
    await apply_migrations(session, MigrationMethod.UP)

    try:
        yield repo
    finally:
        await apply_migrations(session, MigrationMethod.DOWN)
        await repo.close()


@fixture
def links() -> tuple[Link, ...]:
    return (
        Link(link='vk.com'),
        Link(link='habr.com'),
        Link(link='ya.ru'),
        Link(link='google.com'),
        Link(link='google.com'),
    )
