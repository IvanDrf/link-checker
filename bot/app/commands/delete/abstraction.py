from typing import Protocol


class IDeleter(Protocol):
    async def delete_link(self, user_id: int, link: str) -> str: ...
