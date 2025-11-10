from sqlalchemy.ext.asyncio import AsyncEngine
from aiogram import Bot

from app.handlers.handler.handler import Handler
from app.config.config import Config
from app.repo.repo import Repo
from app.database.database import create_engine_for_database


class App:
    def __init__(self, bot: Bot, handler: Handler) -> None:
        self.bot: Bot = bot
        self.handler: Handler = handler

    @classmethod
    async def new(cls, cfg: Config) -> 'App':
        async_engine: AsyncEngine = await create_engine_for_database(cfg)
        repo: Repo = Repo(async_engine)
        handler: Handler = await Handler.new(cfg, repo)

        bot: Bot = Bot(token=cfg.app.bot_token)
        return cls(bot, handler)

    async def run(self) -> None:
        self.handler.register_routes()
        await self.handler.dp.start_polling(self.bot)
