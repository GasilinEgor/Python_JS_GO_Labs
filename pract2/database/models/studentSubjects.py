from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint


class StudentSubjects(Base):
    __tablename__ = "student_subjects"
    student_subjects_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("universitySubjects.subject_id"), nullable=False)
    __table_args__ = (UniqueConstraint("student_id", "subject_id", name="unique_student_subject"),)