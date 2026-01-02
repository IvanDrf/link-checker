from src.core.settings.postgresql import DatabaseSettings
from src.database.postgresql import connect_to_database
from src.repo.links import LinkRepo
from src.service.abstraction import ILinkRepo


class LinkRepoFabric:
    @staticmethod
    async def new_repo(settings: DatabaseSettings) -> ILinkRepo:
        session_maker = await connect_to_database(settings)
        return LinkRepo(session_maker)
