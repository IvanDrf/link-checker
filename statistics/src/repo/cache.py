from json import dumps
from typing import Final, Optional
import logging

from redis.asyncio import Redis, RedisError

from src.schemas.link import Link, Links


LINKS_KEY: Final = 'popular_links'
LINKS_LIFE_TIME: Final = 300


class CacheRepo:
    __slots__ = ('redis')

    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

    async def close(self) -> None:
        await self.redis.aclose()

    async def save_links(self, links: tuple[Link, ...]) -> None:
        links_json = format_links_to_json(links)

        try:
            await self.redis.set(name=LINKS_KEY, value=links_json)
            await self.redis.expire(name=LINKS_KEY, time=LINKS_LIFE_TIME)
        except RedisError as e:
            logging.error(f'redis error: {e.__str__()}')

    async def get_links(self) -> Optional[tuple[Link, ...]]:
        links_json: Optional[str] = await self.redis.get(LINKS_KEY)
        if links_json is None:
            return None

        return Links.validate_json(links_json)


def format_links_to_json(links: tuple[Link, ...]) -> str:
    return dumps([link.model_dump() for link in links])
