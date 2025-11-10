from pydantic import BaseModel, Field


class LinkStatus(BaseModel):
    link: str
    status: bool


class LinkRequest(BaseModel):
    user_id: int = Field(alias='user_id')
    chat_id: int = Field(alias='chat_id')
    links: list[LinkStatus] = Field(alias='links')


class LinkResponse(BaseModel):
    user_id: int = Field(alias='user_id')
    chat_id: int = Field(alias='chat_id')

    links: list[LinkStatus] = Field(alias='links')
