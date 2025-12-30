import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Response, status

from src.api.abstraction import ILinkService
from src.core.exc.internal import InternalError
from src.dependencies.service import get_link_service
from src.schemas.error import ErrorResponse
from src.schemas.link import Link


links_router = APIRouter(prefix='/links')


@links_router.post('/save')
async def save_links(links: Annotated[tuple[Link, ...], Body()], link_service: Annotated[ILinkService, Depends(get_link_service)], response: Response):
    try:
        await link_service.add_links(links)
        response.status_code = status.HTTP_204_NO_CONTENT
    except InternalError as e:
        logging.error(e.__str__())

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponse(message='internal error, cant save links')


@links_router.get('/popluar')
async def get_popular_links(limit: Annotated[int, Query(ge=0, le=50)], link_service: Annotated[ILinkService, Depends(get_link_service)], response: Response):
    try:
        links = await link_service.get_most_popular_links(limit)

        response.status_code = status.HTTP_200_OK
        return links

    except InternalError as e:
        logging.error(e.__str__())

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponse(message='internal error, cant find popular links')


@links_router.get('/')
async def get_links(limit: Annotated[int, Query(ge=0, le=50)], link_service: Annotated[ILinkService, Depends(get_link_service)], response: Response):
    try:
        links = await link_service.get_links(limit)

        response.status_code = status.HTTP_200_OK
        return links
    except InternalError as e:
        logging.error(e.__str__())

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponse(message='internal error, cant find most popular links')
