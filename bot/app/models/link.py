from typing import Final

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.models import Base


MAX_LINK_LENGTH: Final = 150


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(MAX_LINK_LENGTH), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
