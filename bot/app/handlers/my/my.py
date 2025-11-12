from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from typing import Optional

from app.repo.repo import Repo
from app.commands.my.my import MyLinker
from app.models.link import Link

user_links_router: Router = Router()


class UserLinksHandler:
    def __init__(self, repo: Repo) -> None:
        self.linker: MyLinker = MyLinker(repo)

        user_links_router.message(Command('my'))(self.print_user_links)

    async def print_user_links(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        links: Optional[tuple[Link, ...]] = await self.linker.find_user_links(message.from_user.id)
        if links is None or len(links) == 0:
            await message.answer('You dont have saved links, write /save to save some')
            return

        await message.answer(create_links_list(links))


def create_links_list(links: tuple[Link, ...]) -> str:
    return '\n'.join(f'{i+1}) {link.link}' for i, link in enumerate(links))
