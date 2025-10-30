from asyncio import run

from app.config.config import Config
from app.database.database import create_engine


async def main():
    cfg: Config = Config.new(Config.get_config_path_from_flag())
    async_engine = await create_engine(cfg)


if __name__ == '__main__':
    run(main=main())
