from src.repo.links import LinkRepo
from src.service.abstraction import ILinkRepo


class LinkRepoFabric:
    @classmethod
    async def new_repo(cls) -> ILinkRepo:
        return LinkRepo()
