from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, create_engine
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Base(DeclarativeBase):
    pass


class GenerativeTable(Base):
    __tablename__ = 'generate_data'

    field_id: Mapped[UUID] = mapped_column(primary_key=True, autoincrement=False)
    ip: Mapped[str] = mapped_column(String(15), primary_key=True)
    port: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


def make_db_engine(db_url: str, workers: int = 1):
    engine = create_engine(
        db_url,
        pool_size=workers,
        max_overflow=0,
        pool_pre_ping=True
    )
    Base.metadata.create_all(engine)

    return engine


def make_async_db_engine(db_url: str, workers: int) -> AsyncEngine:
    engine = create_async_engine(db_url, pool_size=workers, max_overflow=0)

    return engine
