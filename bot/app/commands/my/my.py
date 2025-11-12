from typing import Optional

from app.repo.repo import Repo
from app.models.link import Link


class MyLinker:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def find_user_links(self, user_id: int) -> Optional[tuple[Link, ...]]:
        links: Optional[tuple[Link, ...]] = await self.repo.find_links(user_id)
        return links
