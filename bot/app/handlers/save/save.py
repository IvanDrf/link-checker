from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.repo.repo import Repo
from app.commands.save.save import Saver
from app.commands.save.state import SaveState

save_router: Router = Router()


class SaveHandler:
    def __init__(self, repo: Repo) -> None:
        self.saver: Saver = Saver(repo)

        save_router.message(Command('save'))(self.input_saved_link)
        save_router.message(SaveState.waiting_input_link)(self.save_link)

    async def input_saved_link(self, message: Message, state: FSMContext) -> None:
        await self.saver.input_link(message, state)

    async def save_link(self, message: Message, state: FSMContext) -> None:
        await self.saver.save_link(message, state)
