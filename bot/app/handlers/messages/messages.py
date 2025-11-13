from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

message_router: Router = Router()


class MessageHandler:
    def __init__(self) -> None:
        message_router.message(F.text)(self.answer)
        message_router.message(F.sticker)(self.answer)
        message_router.message(F.voice)(self.answer)
        message_router.message(F.photo)(self.answer)

    async def answer(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Sorry, but I dont get it, write /help to see available commands', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f'Sorry {message.from_user.first_name}, but I dont get it, write /help to see available commands', reply_markup=ReplyKeyboardRemove())
