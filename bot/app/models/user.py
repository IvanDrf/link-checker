from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger

from app.models.models import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    links_amount: Mapped[int] = mapped_column(nullable=False, default=0)
