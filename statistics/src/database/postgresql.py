from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.settings.settings import settings


_dsn = f'postgresql+asyncpg://{settings.database.user}:{settings.database.password}@{settings.database.host}:{settings.database.port}/{settings.database.db_name}'
_engine = create_async_engine(_dsn)


session_maker = async_sessionmaker(_engine, expire_on_commit=False)
