from src.api.routes.health import health_router
from src.api.routes.links import links_router


routers = (links_router, health_router)
