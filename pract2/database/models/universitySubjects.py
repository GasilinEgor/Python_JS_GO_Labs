from base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class UniversitySubjects(Base):
    __tablename__ = 'universitySubjects'
    subject_id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(30), nullable=False)