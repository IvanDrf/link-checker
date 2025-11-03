from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.repo.repo import Repo
from app.commands.delete.delete import Deleter
from app.commands.delete.state import DeleteState

delete_router: Router = Router()


class DeleteHandler:
    def __init__(self, repo: Repo) -> None:
        self.deleter: Deleter = Deleter(repo)

        delete_router.message(Command('del'))(self.input_deleted_link)
        delete_router.message(DeleteState.waiting_input_link)(self.delete_link)

    async def input_deleted_link(self, message: Message, state: FSMContext) -> None:
        await self.deleter.input_deleted_link(message, state)

    async def delete_link(self, message: Message, state: FSMContext) -> None:
        await self.deleter.delete_link(message, state)
