from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart

from app.repo.repo import Repo
from app.commands.start.start import Starter

start_router: Router = Router()


class StartHandler:
    def __init__(self, repo: Repo) -> None:
        self.starter: Starter = Starter(repo)
        start_router.message(CommandStart())(self.start)

    async def start(self, message: Message, state: FSMContext) -> None:
        await self.starter.start(message, state)
