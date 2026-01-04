from typing import Protocol, Optional

from src.models.link import LinkOrm
from src.schemas.link import Link


class ILinkRepo(Protocol):
    async def add_links(
        self, links: tuple[dict[str, str | int | bool], ...]) -> None: ...

    async def get_most_popular_links(
        self, limit: int) -> tuple[LinkOrm, ...]: ...


class ICacheRepo(Protocol):
    async def save_links(self, links: tuple[Link, ...]) -> None: ...
    async def get_links(self) -> Optional[tuple[Link, ...]]: ...
