from typing import Optional


from pytest import mark

from redis.asyncio import Redis

from src.service.abstraction import ICacheRepo
from src.repo.cache import LINKS_KEY, format_links_to_json


def test_format_links_to_json(links, links_json) -> None:
    links_json_from_format = format_links_to_json(links)
    assert links_json_from_format == links_json


@mark.asyncio
async def test_save_links(cache_repo: ICacheRepo, redis: Redis, links, links_json) -> None:
    await cache_repo.save_links(links)

    links_json_from_cache: Optional[bytes] = await redis.get(LINKS_KEY)

    assert links_json_from_cache is not None
    assert links_json_from_cache.decode() == links_json
