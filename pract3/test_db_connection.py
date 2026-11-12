import traceback

from model import make_db_engine
from sqlalchemy import text


DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/pract3"

try:
    engine = make_db_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Результат запроса:", result.scalar())
        print("Подключение к PostgreSQL успешно!")

except Exception:
    traceback.print_exc()
