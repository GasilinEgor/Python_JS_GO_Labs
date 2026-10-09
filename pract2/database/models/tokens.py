from ..base import Base
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String, DateTime

class Tokens(Base):
    __tablename__ = "tokens"
    token_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
