from typing import Protocol, Optional

from app.models.user import User
from app.models.link import Link
from app.models.message import LinkMessage, LinkStatus


class IRepo(Protocol):
    async def add_user(
        self, user_id: int) -> Optional[int]: ...

    async def find_user(
        self, user_id: int) -> Optional[User]: ...

    async def add_links_amount(
        self, user_id: int, links_amount: int) -> Optional[User]: ...

    async def reduce_links_amount(
        self, user_id: int, links_amount: int) -> Optional[User]: ...

    async def find_links(
        self, user_id: int) -> Optional[tuple[Link, ...]]: ...

    async def save_link(
        self, link: str, user_id: int) -> Optional[int]: ...

    async def delete_link(
        self, link: str, user_id: int) -> Optional[int]: ...


class IRedisRepo(Protocol):
    async def save_links(self, user_id: int, links: LinkMessage) -> None: ...
    async def get_links(self, user_id: int) -> tuple[LinkStatus, ...]: ...
    async def close(self) -> None: ...
