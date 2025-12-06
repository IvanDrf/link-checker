from dataclasses import dataclass, fields

from app.handlers.start.start import StartHandler
from app.handlers.help.help import HelpHandler
from app.handlers.save.save import SaveHandler
from app.handlers.delete.delete import DeleteHandler
from app.handlers.messages.messages import MessageHandler
from app.handlers.my.my import UserLinksHandler
from app.handlers.check.check import CheckHandler
from app.handlers.csv.csv import CsvHandler


@dataclass
class Handlers:
    start: StartHandler
    help: HelpHandler
    save: SaveHandler
    delete: DeleteHandler
    user_links: UserLinksHandler
    check: CheckHandler
    csv: CsvHandler
    message: MessageHandler

    def __iter__(self):
        for handler in fields(self):
            yield (getattr(self, handler.name))
