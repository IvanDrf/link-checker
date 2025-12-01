from typing import Protocol, Final

DEFAULT_ANSWER: Final = ''


class IStarter(Protocol):
    async def start(self, user_id: int) -> str: ...
