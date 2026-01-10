from asyncio import gather
from typing import Any, Final

from fastapi import status
from httpx import ASGITransport, AsyncClient, Response
from pytest import mark, fail

from src.api.abstraction import ILinkService
from src.app.main import app
from src.dependencies.service import get_link_service
from src.schemas.link import Link

from tests.routes.conftest import LinkServiceTest

REPEATED_REQUESTS: Final = 3

link_service: ILinkService = LinkServiceTest()


def get_test_link_service() -> ILinkService:
    global link_service

    return link_service


app.dependency_overrides.update({
    get_link_service: get_test_link_service
})


@mark.asyncio
async def test_save_links(contents: tuple[dict]) -> None:
    async def send_post(json: Any) -> Response:
        response = await client.post('/links/save', json=json)
        return response

    async with AsyncClient(transport=ASGITransport(app), base_url='http://test') as client:
        responses = await gather(*(send_post(contents) for _ in range(REPEATED_REQUESTS)), return_exceptions=True)

        for response in responses:
            if isinstance(response, BaseException):
                fail(f'unexpected exception: {response.__str__()}')

            assert response.status_code == status.HTTP_204_NO_CONTENT

        # invalid bodies
        responses = await gather(send_post(''), send_post([{'name': 'user'}]), return_exceptions=True)
        for response in responses:
            if isinstance(response, BaseException):
                fail(f'unexpected exception: {response.__str__()}')

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@mark.asyncio
async def test_get_most_popular_links() -> None:
    async def send_get(limit: int) -> Response:
        response = await client.get(f'/links/popular?limit={limit}')
        return response

    limits = (10, 5, 2)
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        responses = await gather(*(send_get(limit) for limit in limits), return_exceptions=True)

        for i, response in enumerate(responses):
            if isinstance(response, BaseException):
                fail(f'unexpected exception: {response.__str__()}')

            links_json: list[dict] = response.json()
            links = [Link(**link) for link in links_json]

            assert len(links) <= limits[i]
            assert links[0].views == REPEATED_REQUESTS
