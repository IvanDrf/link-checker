from typing import Protocol

from src.models.link import LinkOrm


class ILinkRepo(Protocol):
    async def add_links(
        self, links: tuple[dict[str, str | int | bool], ...]) -> None: ...

    async def get_most_popular_links(
        self, limit: int) -> tuple[LinkOrm, ...]: ...
