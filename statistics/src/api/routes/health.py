from fastapi import APIRouter, Response, status


health_router = APIRouter()


@health_router.get('/health')
async def get_server_status(response: Response) -> None:
    response.status_code = status.HTTP_204_NO_CONTENT
