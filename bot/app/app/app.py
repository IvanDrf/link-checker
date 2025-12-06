from aiogram import Bot

from app.handlers.handler.handler import Handler
from app.fabric.handlers.handler import HandlerFabric
from app.config.config import Config


class App:
    def __init__(self, bot: Bot, handler: Handler) -> None:
        self.bot: Bot = bot
        self.handler: Handler = handler

    @classmethod
    async def new(cls, cfg: Config) -> 'App':
        handler: Handler = await HandlerFabric.new_handler(cfg)

        bot: Bot = Bot(token=cfg.app.bot_token)
        return cls(bot, handler)

    async def run(self) -> None:
        self.handler.register_routes()
        await self.handler.dp.start_polling(self.bot)

    async def stop(self) -> None:
        await self.handler.stop_handling()
        await self.bot.session.close()
