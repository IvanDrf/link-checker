from typing import Final

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.models import Base


MAX_LINKS_AMOUNT: Final = 10


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    links_amount: Mapped[int] = mapped_column(nullable=False, default=0)
