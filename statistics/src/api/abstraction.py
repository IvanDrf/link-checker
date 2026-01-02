from typing import Protocol

from src.schemas.link import Link


class ILinkService(Protocol):
    async def add_links(self, links: tuple[Link, ...]) -> None: ...

    async def get_most_popular_links(
        self, limit: int) -> tuple[Link, ...]: ...
