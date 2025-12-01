from pydantic import BaseModel, TypeAdapter, Field


class LinkStatus(BaseModel):
    link: str
    status: bool


LinkTuple = TypeAdapter(tuple[LinkStatus, ...])


class LinkMessage(BaseModel):
    user_id: int = Field(alias='user_id')
    chat_id: int = Field(alias='chat_id')
    links: tuple[LinkStatus, ...] = Field(alias='links')
