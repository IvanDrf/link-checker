from asyncio import gather

from fastapi import status
from httpx import ASGITransport, AsyncClient
from pytest import fail, mark

from src.api.abstraction import ILinkService
from src.app.main import app
from src.dependencies.service import get_link_service
from src.schemas.link import Link
from tests.routes.conftest import LinkServiceTest
from tests.routes.utils import send_get, send_post
from tests.utils import is_links_sorted_by_views


__link_service: ILinkService = LinkServiceTest()


def get_test_link_service() -> ILinkService:
    return __link_service


app.dependency_overrides.update({
    get_link_service: get_test_link_service
})


@mark.asyncio
async def test_save_links(contents: tuple[dict], repeated: int) -> None:
    async with AsyncClient(transport=ASGITransport(app), base_url='http://test') as client:
        gather(
            send_valid_post_requests(client, contents, repeated),
            send_invalid_post_requests(client)
        )


async def send_valid_post_requests(client: AsyncClient, contents: tuple[dict], repeated: int) -> None:
    responses = await gather(*(send_post(client, contents) for _ in range(repeated)), return_exceptions=True)

    for response in responses:
        if isinstance(response, BaseException):
            fail(f'unexpected exception: {response.__str__()}')

        assert response.status_code == status.HTTP_204_NO_CONTENT


async def send_invalid_post_requests(client: AsyncClient) -> None:
    responses = await gather(send_post(client, ''), send_post(client, [{'name': 'user'}]), return_exceptions=True)
    for response in responses:
        if isinstance(response, BaseException):
            fail(f'unexpected exception: {response.__str__()}')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@mark.asyncio
async def test_get_most_popular_links(contents: tuple[dict], repeated: int, limits: tuple[int, ...]) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        # send some links
        await send_valid_post_requests(client, contents, repeated)

        responses = await gather(*(send_get(client, limit) for limit in limits), return_exceptions=True)

        for response, limit in zip(responses, limits):
            if isinstance(response, BaseException):
                fail(f'unexpected exception: {response.__str__()}')

            links_json: list[dict] = response.json()
            links = [Link(**link) for link in links_json]
            for link in links:
                print(link.link, link.views)

            assert len(links) == limit
            assert is_links_sorted_by_views(links) is True
