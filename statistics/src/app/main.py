import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from src.api.routers import routers
from src.app.app import close_app, include_routers, init_app
from src.core.settings.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app()
    logging.info(f'Starting app on {settings.app.port}')

    yield

    await close_app()
    logging.info(f'Stopping app on {settings.app.port}')


app = FastAPI(lifespan=lifespan)
include_routers(app, routers)


def main() -> None:
    run(app=app, host=settings.app.host, port=settings.app.port)


if __name__ == '__main__':
    main()
