from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.commands.delete.abstraction import IDeleter
from app.handlers.delete.state import DeleteState

delete_router: Router = Router()


class DeleteHandler:
    def __init__(self, deleter: IDeleter) -> None:
        self.deleter: IDeleter = deleter

        delete_router.message(Command('del'))(self.input_deleted_link)
        delete_router.message(DeleteState.waiting_input_link)(self.delete_link)

    async def input_deleted_link(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer('Enter the link ,you want to delete', reply_markup=ReplyKeyboardRemove())
        await state.set_state(DeleteState.waiting_input_link)

    async def delete_link(self, message: Message, state: FSMContext) -> None:
        if message.text is None or message.from_user is None:
            await message.answer('Cant get your message, try again', reply_markup=ReplyKeyboardRemove())
            return

        message_answer: str = await self.deleter.delete_link(message.from_user.id, message.text)
        await message.answer(message_answer, reply_markup=ReplyKeyboardRemove())

        await state.clear()

    async def stop_handling(self) -> None:
        pass
