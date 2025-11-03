from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class Messenger:
    @staticmethod
    async def Answer(message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Sorry, but I dont get it, write /help to see available commands')
        else:
            await message.answer(f'Sorry {message.from_user.first_name}, but I dont get it, write /help to see available commands')
