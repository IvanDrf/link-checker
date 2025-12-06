from asyncio import run, create_task, Task

from app.config.config import Config
from app.logger.logger import configure_logger
from app.app.app import App


async def main() -> None:
    cfg: Config = Config.load(Config.get_config_path_from_flag())
    configure_logger(cfg)

    app: App = await App.new(cfg)

    app_task: Task = create_task(app.run())
    try:
        await app_task
    finally:
        await app.stop()

if __name__ == '__main__':
    run(main=main())
