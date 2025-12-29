from src.core.settings.settings import Settings
from src.database.cassandra import connect_to_cassandra
from src.repo.links import LinkRepo
from src.service.abstraction import ILinkRepo


class LinkRepoFabric:
    @classmethod
    async def new_repo(cls, settings: Settings) -> ILinkRepo:
        cluster, session = await connect_to_cassandra(settings)

        return LinkRepo(cluster, session)
