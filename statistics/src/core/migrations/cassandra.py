from enum import Enum
from os import getcwd, listdir
from typing import Final

from aiofiles import open
from async_cassandra import AsyncCassandraSession


MIGRATIONS_DIR: Final = './migrations'


class MigrationMethod(Enum):
    UP = 'up'
    DOWN = 'down'


async def apply_migrations(session: AsyncCassandraSession, method: MigrationMethod) -> None:
    print(getcwd())
    migration_files = _get_migration_files_from_dir(MIGRATIONS_DIR, method)

    for filename in migration_files:
        async with open(filename, 'r') as file:
            migration = await file.read()

            stmt = await session.prepare(migration)
            await session.execute(stmt)


def _get_migration_files_from_dir(dir: str, method: MigrationMethod) -> list[str]:
    return sorted([MIGRATIONS_DIR+'/'+file for file in listdir(dir) if method.value in file])
