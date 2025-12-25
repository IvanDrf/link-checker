from pytest import fixture
from pytest_asyncio import fixture as async_fixture
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config.config import Config
from app.database.sql import create_engine_for_database
from app.models.models import TABLES
from app.repo.repo import Repo


@async_fixture(scope='function')
async def repo(config: Config) -> Repo:
    engine = await create_engine_for_database(config)
    await clear_tables(engine)

    return Repo(engine)


async def clear_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for table in TABLES:
            await conn.execute(text(f'DELETE FROM {table}'))


@fixture
def USER_ID() -> int:
    return 123456789


@fixture
def INVALID_USER_ID() -> int:
    return -1
