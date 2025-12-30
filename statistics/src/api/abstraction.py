from typing import Protocol

from src.api.routes import DEFAULT_LIMIT
from src.schemas.link import Link


class ILinkService(Protocol):
    async def add_links(self, links: tuple[Link, ...]) -> None: ...

    async def get_links(
        self, limit: int = DEFAULT_LIMIT) -> tuple[Link, ...]: ...
    async def get_most_popular_links(
        self, limit: int = DEFAULT_LIMIT) -> tuple[Link, ...]: ...

    async def close(self) -> None: ...
