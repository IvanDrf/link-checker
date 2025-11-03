from asyncio import run

from app.config.config import Config
from app.app.app import App


async def main():
    cfg: Config = Config.new(Config.get_config_path_from_flag())
    app: App = await App.new(cfg)

    await app.run()

if __name__ == '__main__':
    run(main=main())
