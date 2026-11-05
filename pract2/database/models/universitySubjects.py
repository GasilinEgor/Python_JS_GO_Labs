from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class UniversitySubjects(Base):
    __tablename__ = "universitySubjects"
    subject_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    subject_name: Mapped[str] = mapped_column(String(30), nullable=False)
