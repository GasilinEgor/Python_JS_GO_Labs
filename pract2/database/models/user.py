from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.role_id"), nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
