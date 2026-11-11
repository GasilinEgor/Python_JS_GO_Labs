import argparse

def create_parser():
    MODE_CHOICES = ['single', "threading", "multiprocessing", "asyncio"]

    parser = argparse.ArgumentParser(description="CLI утилита для генерации данных для СУБД с 4 режимами работы")
    
    parser.add_argument("--mode", choices=MODE_CHOICES, required=True, help="Режим работы инструмента")
    parser.add_argument("--workers", type=int, help="Количество потоков или процессов")
    parser.add_argument("--db-url", type=str, help="Ссылка на подключение к БД PostgreSQL")

    parser.add_argument("--db-host", type=str, help="Хост подклюсчения к БД")
    parser.add_argument("--db-port", type=int, help="Порт подклюсчения к БД")
    parser.add_argument("--db-user", type=str, help="Username пользователя для подклюсчения к БД")
    parser.add_argument("--db-password", type=str, help="Пароль пользователя для подклюсчения к БД")
    parser.add_argument("--db-name", type=str, help="Название БД")

    parser.add_argument("--rows", type=int, required=True, help="Общее число вставляемых строк")
    parser.add_argument("--unique-file-ids", type=int, required=True, help="Число уникальных полей")
    parser.add_argument("--batch-size", type=int, required=True, help="Количество стро в одном INSERT")
    parser.add_argument("--log-file", type=str, required=False, help="Путь к файлу для записи логов", default="insert.log")
    parser.add_argument("--results-file", type=str, required=False, help="Путь к файлу с итогами записи", default="results.log")
    return parser