from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.config import Config
from app.models.models import Base


async def create_engine_for_database(cfg: Config) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        url=f'sqlite+aiosqlite:///{cfg.storage_path}', echo=False)

    await __create_tables(engine)

    return engine


async def __create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
