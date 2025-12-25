from pydantic import BaseModel, TypeAdapter


class Link(BaseModel):
    link: str
    status: bool


Links = TypeAdapter(tuple[Link, ...])
