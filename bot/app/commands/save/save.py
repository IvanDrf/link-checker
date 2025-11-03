from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional

from app.repo.repo import Repo
from app.commands.save.state import SaveState
from app.models.user import User, max_links_amount


class Saver:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def input_link(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer('Enter link:')
        await state.set_state(SaveState.waiting_input_link)

    async def save_link(self, message: Message, state: FSMContext) -> None:
        if message.text is None or message.from_user is None:
            await message.answer('Cant get your message, try again')
            return

        user_id: int = message.from_user.id

        user: Optional[User] = await self.repo.find_user(user_id)
        if user is None:
            await message.answer('You are not in database, please write /start')
            return

        if user.links_amount >= max_links_amount:
            await message.answer(f'You have maximum saved links - {max_links_amount}')
            return

        link: str = message.text

        res: Optional[int] = await self.repo.add_link(link, user_id)
        if res is None:
            await message.answer('Cant save your link, please try again')
            return

        await message.answer(f'Successfully save your link: {link}')
        await state.clear()
