from src.api.abstraction import ILinkService
from src.service.abstraction import ILinkRepo
from src.service.links import LinkService


class LinkServiceFabric:
    @classmethod
    async def new_service(cls, repo: ILinkRepo) -> ILinkService:
        return LinkService(repo)
