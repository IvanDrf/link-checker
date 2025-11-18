from typing import Optional

from app.repo.abstraction import IRepo
from app.models.link import Link


class MyLinker:
    def __init__(self, repo: IRepo) -> None:
        self.repo: IRepo = repo

    async def find_user_links(self, user_id: int) -> Optional[tuple[Link, ...]]:
        links: Optional[tuple[Link, ...]] = await self.repo.find_links(user_id)
        return links
