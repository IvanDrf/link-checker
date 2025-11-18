import pytest
from sqlalchemy import text

from tests.repo.fixture import config

from app.config.config import Config
from app.database.sql import create_engine_for_database
from app.models.models import TABLES


@pytest.mark.asyncio
async def test_connection(config: Config) -> None:
    engine = await create_engine_for_database(config)
    assert not (engine is None)


@pytest.mark.asyncio
async def test_tables(config: Config) -> None:
    engine = await create_engine_for_database(config)

    async with engine.begin() as session:
        res = await session.execute(text('''SELECT name FROM sqlite_master WHERE type='table'  '''))
        existing_tables: list[str] = [row[0] for row in res]

        missing_tables: list[str] = [
            table for table in existing_tables if table not in TABLES]

        assert len(missing_tables) == 0
