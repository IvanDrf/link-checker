from aiogram import Dispatcher

from app.handlers.handler.types import Handlers
from app.handlers.start.start import start_router
from app.handlers.help.help import help_router
from app.handlers.save.save import save_router
from app.handlers.delete.delete import delete_router
from app.handlers.messages.messages import message_router
from app.handlers.my.my import user_links_router
from app.handlers.check.check import check_router
from app.handlers.csv.csv import csv_router


class Handler:
    dp: Dispatcher = Dispatcher()

    def __init__(self, handlers: Handlers) -> None:
        self.handlers: Handlers = handlers

    async def stop_handling(self) -> None:
        for handler in self.handlers:
            await handler.stop_handling()

    def register_routes(self) -> None:
        self.dp.include_router(start_router)
        self.dp.include_router(help_router)
        self.dp.include_router(save_router)
        self.dp.include_router(delete_router)
        self.dp.include_router(user_links_router)
        self.dp.include_router(check_router)
        self.dp.include_router(csv_router)

        self.dp.include_router(message_router)
