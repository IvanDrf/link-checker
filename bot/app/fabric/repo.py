from sqlalchemy.ext.asyncio import AsyncEngine

from app.commands.abstraction.repo import IRepo
from app.repo.repo import Repo
from app.config.config import Config
from app.database.sql import create_engine_for_database


class RepoFabric:
    @staticmethod
    async def new_repo(cfg: Config) -> IRepo:
        async_engine: AsyncEngine = await create_engine_for_database(cfg)

        return Repo(async_engine)
