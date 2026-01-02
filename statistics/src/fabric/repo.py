from src.repo.links import LinkRepo
from src.service.abstraction import ILinkRepo


class LinkRepoFabric:
    @staticmethod
    async def new_repo() -> ILinkRepo:
        return LinkRepo()
