from base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String, Integer

class Marks(Base):
    __tablename__ = 'marks'
    marks_id: Mapped[int] = mapped_column(primary_key=True)
    schedule_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    mark: Mapped[int] = mapped_column(Integer(), nullable=False)