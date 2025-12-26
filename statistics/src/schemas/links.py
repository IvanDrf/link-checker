from pydantic import BaseModel, TypeAdapter, Field


class Link(BaseModel):
    link: str
    status: bool = Field(default=False, exclude=True)
    count: int = 0


Links = TypeAdapter(tuple[Link, ...])
