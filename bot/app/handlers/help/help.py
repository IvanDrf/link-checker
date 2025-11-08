from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import Final

from utils.file_loader import read_file

help_router: Router = Router()


class HelpHandler:
    help_static: Final = 'static/help.html'

    def __init__(self) -> None:
        self.text: str = read_file(HelpHandler.help_static)

        help_router.message(Command('help'))(self.help)

    async def help(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer(self.text, parse_mode='HTML')
