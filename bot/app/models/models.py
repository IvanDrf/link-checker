from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

TABLES: set[str] = {'users', 'links'}


class Base(AsyncAttrs, DeclarativeBase):
    pass
