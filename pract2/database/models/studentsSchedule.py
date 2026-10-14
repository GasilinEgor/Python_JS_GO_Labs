from ..base import Base
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Date, Integer, UniqueConstraint


class StudentSchedule(Base):
    __tablename__ = "studentSchedule"
    schedule_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_subjects_id: Mapped[int] = mapped_column(ForeignKey("student_subjects.student_subjects_id"), nullable=False)
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    pair_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    __table_args__ = (UniqueConstraint('student_subjects_id', 'date', 'pair_count', name='unique_student_schedule'),)