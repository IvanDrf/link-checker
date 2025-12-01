from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import Final
from time import time

from app.handlers.check.abstraction import IChecker
from app.exc.internal import InternalError
from app.exc.external import ExternalError
from app.exc.user import UserError

check_router: Router = Router()


class CheckHandler:
    BUTTONS: Final = [
        [KeyboardButton(text='/csv')]
    ]

    def __init__(self, checker: IChecker) -> None:
        self.checker: IChecker = checker

        check_router.message(Command('check'))(self.check_links)

    async def check_links(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        await message.answer('Starting to check links...')

        try:
            start_time: float = time()
            message_answer = await self.checker.check_links(message.from_user.id, message.chat.id)

            await message.answer(message_answer, reply_markup=ReplyKeyboardMarkup(
                keyboard=CheckHandler.BUTTONS, resize_keyboard=True))
            await message.answer(f'Time: {(time() - start_time):.3f} sec')

        except UserError as e:
            message_answer: str = e.__str__()[e.__str__().find(':') + 1:]
            await message.answer(message_answer, reply_markup=ReplyKeyboardRemove())

        except InternalError as e:
            await message.answer(e.__str__(), reply_markup=ReplyKeyboardRemove())

        except ExternalError as e:
            await message.answer(e.__str__(), reply_markup=ReplyKeyboardRemove())

    async def stop_handling(self) -> None:
        await self.checker.close()
