from typing import Final, Protocol


DEFAULT_ANSWER: Final = ''


class IStarter(Protocol):
    async def start(self, user_id: int) -> str: ...
