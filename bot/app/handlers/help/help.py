from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

help_handler: Router = Router()


class HelpHandler:
    def __init__(self) -> None:
        help_handler.message(Command('help'))(self.help)

    async def help(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer(f'''
Hello, this is Link-Checker bot!
Available commands:
1) /start - start bot
2) /help - view the list of available commands
3) /save - save your link in database
4) /del - delete your link from database    
''')
