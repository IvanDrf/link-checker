from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional

from app.repo.repo import Repo
from app.commands.delete.state import DeleteState
from app.models.user import User


class Deleter:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def input_deleted_link(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer('Enter the link ,you want to delete')
        await state.set_state(DeleteState.waiting_input_link)

    async def delete_link(self, message: Message, state: FSMContext) -> None:
        if message.text is None or message.from_user is None:
            await message.answer('Cant get your message, try again')
            return

        user_id: int = message.from_user.id

        user: Optional[User] = await self.repo.find_user(user_id)
        if user is None:
            await message.answer('You are not in database, please write /start')
            return

        if user.links_amount == 0:
            await message.answer('You dont have any saved links')
            return

        link: str = message.text

        res = await self.repo.delete_link(link, user_id)
        if res is None:
            await message.answer(f'Cant delete this link: {link}')
            return

        await message.answer(f'Successfully deleted your link: {link}')
        await state.clear()
