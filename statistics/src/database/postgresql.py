from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.core.settings.postgresql import DatabaseSettings


async def connect_to_database(settings: DatabaseSettings) -> tuple[async_sessionmaker, AsyncEngine]:
    engine = create_async_engine(settings.dsn)

    return async_sessionmaker(engine, expire_on_commit=False), engine
