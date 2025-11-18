from typing import Protocol, Optional

from app.models.message import LinkMessage


class IConsumer(Protocol):
    async def consume(
        self, user_id: int, chat_id: int) -> Optional[LinkMessage]: ...

    async def close(self) -> None: ...
