from app.config.config import Config
from app.handlers.handler.handler import Handler
from app.handlers.handler.types import Handlers

from app.fabric.dependencies import DependenciesFabric

from app.handlers.start.start import StartHandler
from app.handlers.help.help import HelpHandler
from app.handlers.save.save import SaveHandler
from app.handlers.delete.delete import DeleteHandler
from app.handlers.messages.messages import MessageHandler
from app.handlers.my.my import UserLinksHandler
from app.handlers.check.check import CheckHandler
from app.handlers.csv.csv import CsvHandler


class HandlerFabric:
    @staticmethod
    async def new_handler(cfg: Config) -> Handler:
        deps = await DependenciesFabric.create_handler_dependencies(cfg)

        handlers: Handlers = Handlers(
            start=StartHandler(deps.starter),
            help=HelpHandler(),
            save=SaveHandler(deps.saver),
            delete=DeleteHandler(deps.deleter),
            user_links=UserLinksHandler(deps.my_linker),
            check=CheckHandler(deps.checker),
            csv=CsvHandler(deps.csver),
            message=MessageHandler(),
        )

        return Handler(handlers)
