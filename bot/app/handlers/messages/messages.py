from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.messages.messages import Messenger

message_router: Router = Router()


class MessageHandler:
    def __init__(self) -> None:
        self.messenger: Messenger = Messenger()

        message_router.message(F.text)(self.answer)
        message_router.message(F.sticker)(self.answer)
        message_router.message(F.voice)(self.answer)
        message_router.message(F.photo)(self.answer)

    async def answer(self, message: Message, state: FSMContext) -> None:
        await self.messenger.answer(message, state)
