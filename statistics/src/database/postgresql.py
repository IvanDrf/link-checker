from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.settings.postgresql import DatabaseSettings


async def connect_to_database(settings: DatabaseSettings) -> async_sessionmaker:
    dsn = f'postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}'
    engine = create_async_engine(dsn)

    return async_sessionmaker(engine, expire_on_commit=False)
