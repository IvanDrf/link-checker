from asyncio import gather

from fastapi import status
from httpx import ASGITransport, AsyncClient
from pytest import mark

from src.app.main import app


@mark.asyncio
async def test_health_check(repeated: int) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        responses = await gather(*(client.get('/health') for _ in range(repeated)))

        for response in responses:
            assert response.status_code == status.HTTP_204_NO_CONTENT
