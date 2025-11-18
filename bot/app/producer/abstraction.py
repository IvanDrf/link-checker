from typing import Protocol

from app.models.message import LinkMessage


class IProducer(Protocol):
    async def produce(self, links: LinkMessage) -> None: ...
    async def close(self) -> None: ...
