from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import Final

from utils.file_reader import read_file

help_router: Router = Router()


class HelpHandler:
    HELP_STATIC: Final = 'static/help.html'

    def __init__(self) -> None:
        self.help_text: str = read_file(HelpHandler.HELP_STATIC)

        help_router.message(Command('help'))(self.help)

    async def help(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer(self.help_text, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

    async def stop_handling(self) -> None:
        pass
