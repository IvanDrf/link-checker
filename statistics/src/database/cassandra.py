from async_cassandra import AsyncCassandraSession, AsyncCluster

from src.core.settings.settings import Settings


async def connect_to_cassandra(settings: Settings) -> tuple[AsyncCluster, AsyncCassandraSession]:
    cluster = AsyncCluster([settings.cassandra.host],
                           port=settings.cassandra.port)

    session = await cluster.connect(settings.cassandra.key_space)

    return cluster, session
