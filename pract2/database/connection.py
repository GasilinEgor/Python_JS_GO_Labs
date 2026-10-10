from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL не найден")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()
