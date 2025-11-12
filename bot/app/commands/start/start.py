from typing import Optional, Final

from app.repo.repo import Repo
from app.models.user import User

DEFAULT_ANSWER: Final = ''


class Starter:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo

    async def start(self, user_id: int) -> str:
        user: Optional[User] = await self.repo.find_user(user_id)
        if user:
            return DEFAULT_ANSWER

        user_id_database: Optional[int] = await self.repo.add_user(user_id)
        if user_id_database is None:
            return 'Cant add you to database, please write /start again'

        return DEFAULT_ANSWER
