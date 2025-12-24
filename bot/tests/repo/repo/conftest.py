from pytest_asyncio import fixture as async_fixture
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from app.config.config import Config
from app.database.sql import create_engine_for_database
from app.repo.repo import Repo
from app.models.models import TABLES


@async_fixture(scope='package')
async def repo(config: Config) -> Repo:
    engine = await create_engine_for_database(config)
    await clear_tables(engine)

    return Repo(engine)


async def clear_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for table in TABLES:
            await conn.execute(text(f'DELETE FROM {table}'))
