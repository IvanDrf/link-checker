from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


TABLES: set[str] = {'users', 'links'}


class Base(AsyncAttrs, DeclarativeBase):
    pass
