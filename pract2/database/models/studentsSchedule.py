from base import Base
from datetime import date
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String, Date, Integer


class StudentSchedule(Base):
    __tablename__ = "studentSchedule"
    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('universitySubjects.subject_id'), nullable=False)
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    pair_count: Mapped[int] = mapped_column(Integer(), nullable=False)