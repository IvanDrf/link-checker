from aiogram import Dispatcher

from app.commands.check.check import Checker

from app.config.config import Config
from app.handlers.start.start import StartHandler, start_router
from app.handlers.help.help import HelpHandler, help_router
from app.handlers.save.save import SaveHandler, save_router
from app.handlers.delete.delete import DeleteHandler, delete_router
from app.handlers.messages.messages import MessageHandler, message_router
from app.handlers.my.my import UserLinksHandler, user_links_router
from app.handlers.check.check import CheckHandler, check_router

from app.repo.repo import Repo


class Handler(StartHandler, HelpHandler, SaveHandler, DeleteHandler, UserLinksHandler, CheckHandler, MessageHandler):
    dp: Dispatcher = Dispatcher()

    def __init__(self, repo: Repo, checker: Checker) -> None:
        StartHandler.__init__(self, repo)
        HelpHandler.__init__(self)
        SaveHandler.__init__(self, repo)
        DeleteHandler.__init__(self, repo)
        UserLinksHandler.__init__(self, repo)
        CheckHandler.__init__(self, checker)

        MessageHandler.__init__(self)

    @classmethod
    async def new(cls, cfg: Config, repo: Repo) -> 'Handler':
        checker: Checker = await Checker.new(cfg, repo)
        return cls(repo, checker)

    def register_routes(self) -> None:
        self.dp.include_router(start_router)
        self.dp.include_router(help_router)
        self.dp.include_router(save_router)
        self.dp.include_router(delete_router)
        self.dp.include_router(user_links_router)
        self.dp.include_router(check_router)

        self.dp.include_router(message_router)
