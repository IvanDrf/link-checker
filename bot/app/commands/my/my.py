from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional

from app.repo.repo import Repo
from app.models.link import Link


class MyLinker:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def find_user_links(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        user_id: int = message.from_user.id

        links: Optional[tuple[Link, ...]] = await self.repo.find_links(user_id)
        if links is None or len(links) == 0:
            await message.answer('You dont have saved links, write /save to save some')
            return

        await message.answer(create_links_list(links))


def create_links_list(links: tuple[Link, ...]) -> str:
    return '\n'.join(f'{i+1}) {link.link}' for i, link in enumerate(links))
