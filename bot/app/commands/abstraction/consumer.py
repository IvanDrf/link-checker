from typing import Optional, Protocol

from app.schemas.message import LinkMessage


class IConsumer(Protocol):
    async def consume(
        self, user_id: int, chat_id: int) -> Optional[LinkMessage]: ...

    async def close(self) -> None: ...
