from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.repo.repo import Repo
from app.commands.my.my import MyLinker

user_links_router: Router = Router()


class UserLinksHandler:
    def __init__(self, repo: Repo) -> None:
        self.linker: MyLinker = MyLinker(repo)

        user_links_router.message(Command('my'))(self.print_user_links)

    async def print_user_links(self, message: Message, state: FSMContext) -> None:
        await self.linker.find_user_links(message, state)
