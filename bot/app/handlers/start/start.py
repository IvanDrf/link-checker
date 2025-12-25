from typing import Final

from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.handlers.start.abstraction import DEFAULT_ANSWER, IStarter
from utils.file_reader import read_file


start_router: Router = Router()


class StartHandler:
    START_STATIC: Final = 'static/start.html'

    def __init__(self, starter: IStarter) -> None:
        self.start_text: str = read_file(StartHandler.START_STATIC)
        self.starter: IStarter = starter

        start_router.message(CommandStart())(self.start)

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        message_answer: str = await self.starter.start(message.from_user.id)
        if message_answer == DEFAULT_ANSWER:
            await message.answer(self.start_text.format(username=message.from_user.first_name), parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
            return

        message.answer(message_answer, reply_markup=ReplyKeyboardRemove())

    async def stop_handling(self) -> None:
        pass
