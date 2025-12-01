from typing import Optional

from app.commands.abstraction.repo import IRepo
from app.models.user import User


class Deleter:
    def __init__(self, repo: IRepo) -> None:
        self.repo: IRepo = repo

    async def delete_link(self, user_id: int, link: str) -> str:
        user: Optional[User] = await self.repo.find_user(user_id)
        if user is None:
            return 'You are not in database, please write /start'

        if user.links_amount == 0:
            return 'You dont have any saved links'

        res = await self.repo.delete_link(link, user_id)
        if res is None:
            return f'Cant delete this link: {link}'

        return f'Successfully deleted your link: {link}'
