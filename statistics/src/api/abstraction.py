from typing import Protocol

from src.schemas.link import Link


class ILinkService(Protocol):
    async def add_links(self, links: tuple[Link, ...]) -> None: ...
    async def close(self) -> None: ...
