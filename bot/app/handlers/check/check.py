from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.config.config import Config
from app.repo.repo import Repo
from app.commands.check.check import Checker
from app.exc.internal import InternalError

check_router: Router = Router()


class CheckHandler:
    def __init__(self, checker: Checker) -> None:
        self.checker: Checker = checker

        check_router.message(Command('check'))(self.check_links)

    @classmethod
    async def new(cls, cfg: Config, repo: Repo) -> 'CheckHandler':
        checker: Checker = await Checker.new(cfg, repo)

        return cls(checker)

    async def check_links(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        try:
            message_answer: str = await self.checker.check_links(message.from_user.id, message.chat.id)
            await message.answer(message_answer, reply_markup=ReplyKeyboardRemove())
        except InternalError as e:
            await message.answer(e.__str__(), reply_markup=ReplyKeyboardRemove())
