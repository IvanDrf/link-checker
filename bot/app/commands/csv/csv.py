import logging

from app.repo.abstraction import IRedisRepo
from app.models.message import LinkStatus
from app.exc.internal import InternalError
from app.csv.csv import write_links, remove_links_file


class Csver:
    def __init__(self, redis_repo: IRedisRepo) -> None:
        self.redis_repo: IRedisRepo = redis_repo

    async def get_csv_report(self, user_id: int) -> str:
        '''returns filename'''
        try:
            links: tuple[LinkStatus, ...] = await self.redis_repo.get_links(user_id)
            if len(links) == 0:
                return ''

            return await write_links(user_id, links)

        except InternalError:
            return ''

        except Exception as e:
            logging.error(f'csver unexpected error -> {e.__str__()}')
            return ''

    async def remove_csv_report(self, user_id: int) -> None:
        try:
            await remove_links_file(user_id)

        except Exception as e:
            logging.error(f'csver unexpected error -> {e.__str__()}')
