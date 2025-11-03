from aiogram import Dispatcher

from app.handlers.start.start import StartHandler, start_router
from app.handlers.help.help import HelpHandler, help_handler
from app.handlers.save.save import SaveHandler, save_router
from app.handlers.delete.delete import DeleteHandler, delete_router
from app.handlers.messages.messages import MessageHandler, message_router

from app.repo.repo import Repo


class Handler(StartHandler, HelpHandler, SaveHandler, DeleteHandler, MessageHandler):
    dp: Dispatcher = Dispatcher()

    def __init__(self, repo: Repo) -> None:
        StartHandler.__init__(self, repo)
        HelpHandler.__init__(self)
        SaveHandler.__init__(self, repo)
        DeleteHandler.__init__(self, repo)
        MessageHandler.__init__(self)

    def register_routes(self) -> None:
        self.dp.include_router(start_router)
        self.dp.include_router(help_handler)
        self.dp.include_router(save_router)
        self.dp.include_router(delete_router)

        self.dp.include_router(message_router)
