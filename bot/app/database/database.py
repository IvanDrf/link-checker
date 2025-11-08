from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine

from app.config.config import Config
from app.models.models import Base, tables


async def create_engine_for_database(cfg: Config) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        url=f'sqlite+aiosqlite:///{cfg.app.storage_path}', echo=True)

    await __check_for_missing_tables(engine)

    return engine


async def __check_for_missing_tables(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        res = await conn.execute(text('''SELECT name FROM sqlite_master WHERE type='table' '''))
        existing_tables: list[str] = [row[0] for row in res]

        missing_tables: list[str] = [
            table for table in existing_tables if table not in tables]

        if len(missing_tables) != 0:
            await __create_tables(conn)


async def __create_tables(conn: AsyncConnection) -> None:
    await conn.run_sync(Base.metadata.create_all)
