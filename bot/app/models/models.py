from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

tables: set[str] = {'users', 'links'}


class Base(AsyncAttrs, DeclarativeBase):
    pass
