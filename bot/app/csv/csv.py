from aiocsv import AsyncWriter
from aiofiles import open
from aiofiles.os import remove
from typing import Final

import logging

from app.schemas.message import LinkStatus

CSV_DIR: Final = 'storage/csv'


async def write_links(user_id: int, links: tuple[LinkStatus, ...]) -> str:
    filename: str = create_filename(user_id)

    async with open(filename, mode='w', encoding='utf-8', newline='') as csv_file:
        writer: AsyncWriter = AsyncWriter(csv_file)

        for link in links:
            await writer.writerow([link.link, 'YES' if link.status else 'NO'])

    return filename


async def remove_links_file(user_id: int) -> None:
    filename: str = create_filename(user_id)

    try:
        await remove(filename)
    except Exception as e:
        logging.error(f'Cant remove file: {e.__str__()}')


def create_filename(user_id: int) -> str:
    return f'{CSV_DIR}/{user_id}.csv'
