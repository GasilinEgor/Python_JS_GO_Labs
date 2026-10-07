from base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String


class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.role_id"), nullable=False)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(255), nullable=False)