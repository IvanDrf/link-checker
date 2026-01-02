import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from src.api.routes import links_router
from src.app.app import init_app
from src.core.settings.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info(f'Starting app on {settings.app.port}')
    await init_app()

    yield

    logging.info(f'Stopping app on {settings.app.port}')


app = FastAPI(lifespan=lifespan)
app.include_router(links_router)


def main() -> None:
    run(app=app, host=settings.app.host, port=settings.app.port)


if __name__ == '__main__':
    main()
