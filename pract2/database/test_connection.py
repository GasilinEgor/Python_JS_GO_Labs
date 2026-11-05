import traceback

from connection import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Результат запроса:", result.scalar())
        print("Подключение к PostgreSQL успешно!")

except Exception:
    traceback.print_exc()
