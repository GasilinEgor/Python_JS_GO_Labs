from ..base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Role(Base):
    __tablename__ = 'role'
    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

