from async_cassandra import AsyncCassandraSession, AsyncCluster

from src.repo.links import LinkRepo
from src.service.abstraction import ILinkRepo


class LinkRepoFabric:
    @classmethod
    async def new_repo(cls, cluster: AsyncCluster, session: AsyncCassandraSession) -> ILinkRepo:
        return LinkRepo(cluster, session)
