from typing import Sequence

from src.models.link import LinkOrm
from src.schemas.link import Link


def is_links_are_same(links_from_db: Sequence[LinkOrm], links: Sequence[Link]) -> bool:
    return set(link.link for link in links_from_db) == set(
        link.link for link in links)


def is_links_sorted_by_views(links: Sequence[Link]) -> bool:
    return all(links[i].views >= links[i + 1].views for i in range(len(links) - 1))
