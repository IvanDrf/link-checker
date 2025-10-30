from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from typing import Final

from app.models.models import Base

max_link_length: Final = 150


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(max_link_length), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
