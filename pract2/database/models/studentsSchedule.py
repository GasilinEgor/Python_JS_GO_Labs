from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class StudentSchedule(Base):
    __tablename__ = "studentSchedule"
    schedule_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    student_subjects_id: Mapped[int] = mapped_column(
        ForeignKey("student_subjects.student_subjects_id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    pair_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "student_subjects_id",
            "date",
            "pair_count",
            name="unique_student_schedule",
        ),
    )
