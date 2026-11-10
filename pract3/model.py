from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, create_engine
from datetime import datetime
from uuid import UUID


class Base(DeclarativeBase):
    pass


class GenerativeTable(Base):
    __tablename__ = 'generate_data'

    field_id: Mapped[UUID] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(15), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


def create_engine(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    return engine
