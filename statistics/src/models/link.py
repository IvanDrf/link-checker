from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class LinkOrm(Base):
    __tablename__ = 'links'

    link: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)
