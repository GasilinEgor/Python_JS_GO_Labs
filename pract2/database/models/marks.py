from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Marks(Base):
    __tablename__ = "marks"
    marks_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_subjects_id: Mapped[int] = mapped_column(
        ForeignKey("student_subjects.student_subjects_id"), nullable=False
    )
    mark: Mapped[int] = mapped_column(Integer(), nullable=False)
