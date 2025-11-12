from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart

from typing import Final

from app.repo.repo import Repo
from app.commands.start.start import Starter, DEFAULT_ANSWER
from utils.file_reader import read_file


start_router: Router = Router()


class StartHandler:
    START_STATIC: Final = 'static/start.html'

    def __init__(self, repo: Repo) -> None:
        self.start_text: str = read_file(StartHandler.START_STATIC)
        self.starter: Starter = Starter(repo)

        start_router.message(CommandStart())(self.start)

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        message_answer: str = await self.starter.start(message.from_user.id)
        if message_answer == DEFAULT_ANSWER:
            await message.answer(self.start_text.format(username=message.from_user.first_name), parse_mode='HTML')
            return

        message.answer(message_answer)
