from src.api.abstraction import ILinkService
from src.service.abstraction import ILinkRepo
from src.service.links import LinkService


class LinkServiceFabric:
    @staticmethod
    async def new_service(repo: ILinkRepo) -> ILinkService:
        return LinkService(repo)
