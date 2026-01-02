from typing import Optional

from src.api.abstraction import ILinkService


_link_service: Optional[ILinkService] = None


def init_link_service(service: ILinkService) -> None:
    global _link_service

    if _link_service is None:
        _link_service = service


def get_link_service() -> ILinkService:
    global _link_service

    if _link_service is None:
        raise RuntimeError('links service is not initialized')

    return _link_service
