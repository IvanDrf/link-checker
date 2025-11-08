from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional, Final

from app.repo.repo import Repo
from app.models.user import User
from bot.utils.file_reader import read_file


class Starter:
    start_static: Final = 'static/start.html'

    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

        self.text: str = read_file(Starter.start_static)

    async def start(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        user_id: Optional[int] = message.from_user.id
        user: Optional[User] = await self.repo.find_user(user_id)
        if user:
            await message.answer(self.text.format(username=message.from_user.first_name), parse_mode='HTML')
            return

        user_id = await self.repo.add_user(user_id)
        if user_id is None:
            await message.answer('Cant add you to database, please write /start again')
            return

        await message.answer(f'Hello {message.from_user.first_name}, this is link-checker bot, write /help')
