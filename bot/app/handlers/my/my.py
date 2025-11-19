from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from typing import Optional, Final

from app.models.link import Link
from app.commands.my.abstraction import ILinker

user_links_router: Router = Router()


class UserLinksHandler:
    BUTTONS: Final = [
        [KeyboardButton(text='/save')],
        [KeyboardButton(text='/del')],
        [KeyboardButton(text='/check')]
    ]

    def __init__(self, my_linker: ILinker) -> None:
        self.linker: ILinker = my_linker
        self.keyboard: Final = ReplyKeyboardMarkup(
            keyboard=UserLinksHandler.BUTTONS, resize_keyboard=True, one_time_keyboard=True)

        user_links_router.message(Command('my'))(self.print_user_links)

    async def print_user_links(self, message: Message, state: FSMContext) -> None:
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        links: Optional[tuple[Link, ...]] = await self.linker.find_user_links(message.from_user.id)
        if links is None or len(links) == 0:
            await message.answer('You dont have saved links, write /save to save some')
            return

        await message.answer(create_links_list(links), reply_markup=self.keyboard)

    async def stop_handling(self) -> None:
        pass


def create_links_list(links: tuple[Link, ...]) -> str:
    return '\n'.join(f'{i+1}) {link.link}' for i, link in enumerate(links))
