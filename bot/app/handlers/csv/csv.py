from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.csv.csv import create_filename, remove_links_file
from app.handlers.csv.state import CsvState

csv_router: Router = Router()


class CsvHandler:
    def __init__(self) -> None:
        csv_router.message(Command('csv'))(self.get_csv_report)
        csv_router.message(CsvState.waiting_for_exit)(self.exit_from_csv_mode)

    async def get_csv_report(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        csv_file: FSInputFile = FSInputFile(
            path=create_filename(message.from_user.id))

        await message.answer_document(csv_file, reply_markup=ReplyKeyboardRemove())
        await remove_links_file(message.from_user.id)

    async def exit_from_csv_mode(self, message: Message, state: FSMContext) -> None:
        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        await remove_links_file(message.from_user.id)

        await state.clear()
        await message.answer('You successfully exit from check mode', reply_markup=ReplyKeyboardRemove())
