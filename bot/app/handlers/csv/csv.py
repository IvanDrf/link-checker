from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.handlers.csv.abstraction import ICsver

csv_router: Router = Router()


class CsvHandler:
    def __init__(self, csver: ICsver) -> None:
        self.csver: ICsver = csver

        csv_router.message(Command('csv'))(self.get_csv_report)

    async def get_csv_report(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again', reply_markup=ReplyKeyboardRemove())
            return

        filename: str = await self.csver.get_csv_report(message.from_user.id)
        if filename == '':
            await message.answer('Cant get your checked links, please try /check them again', reply_markup=ReplyKeyboardRemove())
            return

        await self._send_csv_report(message, filename, message.from_user.id)

    async def _send_csv_report(self, message: Message, filename: str, user_id: int) -> None:
        csv_file: FSInputFile = FSInputFile(filename)

        await message.answer_document(csv_file, reply_markup=ReplyKeyboardRemove())
        await self.csver.remove_csv_report(user_id)

    async def stop_handling(self) -> None:
        pass
