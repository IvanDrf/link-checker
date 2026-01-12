from typing import Any

from httpx import AsyncClient, Response


async def send_post(client: AsyncClient, json: Any) -> Response:
    response = await client.post('/links/save', json=json)
    return response


async def send_get(client: AsyncClient, limit: int) -> Response:
    response = await client.get(f'/links/popular?limit={limit}')
    return response
