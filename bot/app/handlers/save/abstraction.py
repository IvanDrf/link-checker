from typing import Protocol


class ISaver(Protocol):
    async def save_link(self, user_id: int, link: str) -> str: ...
