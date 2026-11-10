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


def check_workers_valid(args: argparse.Namespace) -> bool:
    PARALLEL_MODES = ('threading', "multiprocessing", "asyncio")
    if args.mode in PARALLEL_MODES:
        if not args.workers:
            print("Не указан параметр --workers!")
            return False
        
        if args.workers < 1:
            print("Неверное значение параметра workers!")
            return False
    
    return True
    

def check_batch_size_valid(args: argparse.Namespace) -> bool:
    if args.batch_size > args.rows:
        print("Batch_size не должен превышать rows!")
        return False
    
    return True


def check_int_valid(args: argparse.Namespace) -> bool:
    if args.rows < 1:
        print("Неверное значение параметра args!")
        return False
    
    if args.unique_file_ids < 1:
        print("Неверное значение пааметра uniqoe_file_ids!")
        return False
    
    return True


def check_db_creds_valid(args: argparse.Namespace) -> bool:
    credits = [args.db_host, args.db_port, args.db_user, args.db_password, args.db_name]
    if not all(credits):
        print("Не указаны все параметры для подключения к БД")
        return False

    if not(check_port_valid(args.db_port)):
        return False
    
    return True


def check_port_valid(port: int) -> bool:
    if 1 <= port <= 65535:
        print("Некорректное значение параметра db-port!")
        return True
    
    return False


def check_db_url_valid(args: argparse.Namespace) -> bool:
    if not args.db_url:
        if not check_db_creds_valid(args):
            print("Неверное указание параметров ссылки на БД!")
            return False
    
    return True


def check_args_valid(args: argparse.Namespace) -> bool:
    return check_workers_valid(args) and check_batch_size_valid(args) and check_int_valid(args) and check_db_url_valid(args)


def create_db_url(args: argparse.Namespace) -> str:
    return f"postgresql://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}"


def main():
    parser = create_parser()
    args = parser.parse_args()
    if not check_args_valid(args):
        return
    print(args.mode)

if __name__ == '__main__':
    main()