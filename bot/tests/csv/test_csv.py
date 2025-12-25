from pathlib import Path

from aiocsv import AsyncReader
from aiofiles import open
from pytest import mark

from app.csv.csv import CSV_DIR, create_filename, remove_links_file, write_links
from app.schemas.message import LinkStatus


def test_create_filename() -> None:
    for user_id in range(1, 10):
        expected_filename = f'{CSV_DIR}/{user_id}.csv'

        assert create_filename(user_id) == expected_filename


@mark.asyncio
async def test_write_links(USER_ID: int, links: tuple[LinkStatus, ...]) -> None:
    expected_filename = create_filename(USER_ID)

    filename = await write_links(USER_ID, links)

    assert filename == expected_filename
    assert await read_csv_file(filename) == links

    await remove_links_file(USER_ID)


@mark.asyncio
async def test_remove_links_file(USER_ID: int, links: tuple[LinkStatus, ...]) -> None:
    filename = await write_links(USER_ID, links)

    file_path = Path(filename)
    assert file_path.exists() == True

    await remove_links_file(USER_ID)

    assert file_path.exists() == False


async def read_csv_file(filename: str) -> tuple[LinkStatus, ...]:
    async with open(filename, 'r') as file:
        reader = AsyncReader(file)

        return tuple([LinkStatus(
            link=string[0], status=True if string[1] == 'YES' else False) async for string in reader])
