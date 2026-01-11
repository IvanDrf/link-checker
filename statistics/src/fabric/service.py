from src.api.abstraction import ILinkService
from src.service.abstraction import ICacheRepo, ILinkRepo
from src.service.links import LinkService


class LinkServiceFabric:
    @staticmethod
    def new_service(link_repo: ILinkRepo, cache_repo: ICacheRepo) -> ILinkService:
        return LinkService(link_repo, cache_repo)
