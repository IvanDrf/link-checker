from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import Final

from app.config.config import Config
from app.repo.repo import Repo
from app.commands.check.check import Checker
from app.exc.internal import InternalError
from app.exc.external import ExternalError
from app.exc.user import UserError
from app.csv.csv import write_links
from app.handlers.csv.state import CsvState

check_router: Router = Router()


class CheckHandler:
    BUTTONS: Final = [
        [KeyboardButton(text='/csv')]
    ]

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
            links, message_answer = await self.checker.check_links(message.from_user.id, message.chat.id)

            await message.answer(message_answer, reply_markup=ReplyKeyboardMarkup(
                keyboard=CheckHandler.BUTTONS, resize_keyboard=True))

            await message.answer('Enter /csv to get csv report for this links, or /exit to exit from check mode')
            await state.set_state(CsvState.waiting_for_exit)

            await write_links(message.from_user.id, links)

        except UserError as e:
            message_answer: str = e.__str__()[e.__str__().find(':') + 1:]
            await message.answer(message_answer, reply_markup=ReplyKeyboardRemove())

        except InternalError as e:
            await message.answer(e.__str__(), reply_markup=ReplyKeyboardRemove())

        except ExternalError as e:
            await message.answer(e.__str__(), reply_markup=ReplyKeyboardRemove())
