from typing import Optional, Protocol

from app.models.link import Link


class ILinker(Protocol):
    async def find_user_links(
        self, user_id: int) -> Optional[tuple[Link, ...]]: ...
