from sqlalchemy import text
from connection import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Результат запроса:", result.scalar())
        print("Подключение к PostgreSQL успешно!")

except Exception as e:
    print("Ошибка подключения к PostgreSQL")
    print(e)