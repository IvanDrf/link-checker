import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import run

from src.api.routes import links_router
from src.core.logger.logger import setup_logger
from src.core.settings.settings import settings
from src.dependencies.service import get_link_service, init_link_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info(f'Starting app on {settings.app.port}')
    await init_link_service()

    yield

    logging.info(f'Stopping app on {settings.app.port}')
    service = await get_link_service()
    await service.close()


app = FastAPI(lifespan=lifespan)
app.include_router(links_router)


def main() -> None:
    setup_logger()
    run(app=app, host=settings.app.host, port=settings.app.port)


if __name__ == '__main__':
    main()
