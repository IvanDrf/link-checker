from aiogram import Dispatcher

from app.handlers.start.start import StartHandler
from app.handlers.start.start import start_router
from app.repo.repo import Repo


class Handler(StartHandler):
    dp: Dispatcher = Dispatcher()

    def __init__(self, repo: Repo) -> None:
        StartHandler.__init__(self, repo)

    def register_routes(self) -> None:
        self.dp.include_router(start_router)
