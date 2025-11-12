from typing import Optional

from app.repo.repo import Repo
from app.models.user import User, MAX_LINKS_AMOUNT


class Saver:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def save_link(self, user_id: int, link: str) -> str:
        user: Optional[User] = await self.repo.find_user(user_id)
        if user is None:
            return 'You are not in database, please write /start'

        if user.links_amount >= MAX_LINKS_AMOUNT:
            return f'You have maximum saved links - {MAX_LINKS_AMOUNT}'

        res: Optional[int] = await self.repo.save_link(link, user_id)
        if res is None:
            return 'Cant save your link, please try again'

        return f'Successfully saved your link: {link}'
