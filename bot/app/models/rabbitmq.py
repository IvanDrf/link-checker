from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class LinkRequest(BaseModel):
    user_id: int = Field(alias='user_id')
    chat_id: int = Field(alias='chat_id')
    links: list[str] = Field(alias='links')


@dataclass
class LinkStatus:
    link: str
    status: bool


@dataclass
class LinkResponse(BaseModel):
    user_id: int = Field(alias='user_id')
    chat_id: int = Field(alias='chat_id')

    links: list[LinkStatus] = Field(alias='links')
