import argparse


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