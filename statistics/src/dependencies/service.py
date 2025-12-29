from typing import Optional

from src.api.abstraction import ILinkService
from src.core.settings.settings import settings
from src.fabric.repo import LinkRepoFabric
from src.fabric.service import LinkServiceFabric


_link_service: Optional[ILinkService] = None


async def init_link_service() -> None:
    global _link_service

    if _link_service is None:
        repo = await LinkRepoFabric.new_repo(settings)
        _link_service = await LinkServiceFabric.new_service(repo)


async def get_link_service() -> ILinkService:
    global _link_service

    if _link_service is None:
        raise RuntimeError('links service is not initialized')

    return _link_service
