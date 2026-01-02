from pydantic import BaseModel, Field, TypeAdapter


class Link(BaseModel):
    link: str
    status: bool = Field(default=False, exclude=True)
    views: int = 0


Links = TypeAdapter(tuple[Link, ...])
