from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.handlers.save.abstraction import ISaver
from app.handlers.save.state import SaveState


save_router: Router = Router()


class SaveHandler:
    def __init__(self, saver: ISaver) -> None:
        self.saver: ISaver = saver

        save_router.message(Command('save'))(self.input_saved_link)
        save_router.message(SaveState.waiting_input_link)(self.save_link)

    async def input_saved_link(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        await message.answer('Enter the link, you want to save')
        await state.set_state(SaveState.waiting_input_link)

    async def save_link(self, message: Message, state: FSMContext) -> None:
        if message.text is None or message.from_user is None:
            await message.answer('Cant get your message, try again')
            return

        message_answer: str = await self.saver.save_link(message.from_user.id, message.text)
        await message.answer(message_answer, reply_markup=ReplyKeyboardRemove())

        await state.clear()

    async def stop_handling(self) -> None:
        pass
