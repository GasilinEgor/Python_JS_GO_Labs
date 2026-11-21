from parser import create_parser
from validation import check_args_valid
from model import make_db_engine
from logger import setup

import asyncio
import argparse
import logging

from modes.single import run as single_run
from modes.threading import run as threading_run
from modes.multiprocessing import run as multiprocessing_run
from modes.asyncio import run as asynco_run




def create_db_url(args: argparse.Namespace) -> str:
    if not args.db_url:
        db_url = f"postgresql://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}"
    else:
        db_url = args.db_url
    return db_url


def save_results(report: dict, result_file: str) -> None:
    text = (
        f"Режим работы: {report["mode"]}\n"
        f"Количество потоков/процессов: {report['workers']}\n"
        f"Вставлено строк: {report["inserted_rows"]}\n"
        f"Время работы: {report["work_time"]}\n"
        f"Максимальные затраты памяти: {report["peak_memory"]} мб\n"
    )

    print(text)

    with open(result_file, "a", encoding='utf-8') as file:
        file.write(text)
        file.write("\n")


def start_single_mode(args: argparse.Namespace) -> dict:
    logger = setup(args.log_file)
    db_url = create_db_url(args)
    engine = make_db_engine(db_url)

    modes_parameters = {
        "engine": engine,
        "rows": args.rows,
        "unique_file_ids": args.unique_file_ids, 
        "batch_size": args.batch_size, 
        "logger": logger
    }

    report = single_run(**modes_parameters)

    return report


def start_threading_mode(args: argparse.Namespace) -> dict:
    logger = setup(args.log_file)
    db_url = create_db_url(args)
    engine = make_db_engine(db_url, args.workers)

    modes_parameters = {
        "engine": engine,
        "rows": args.rows,
        "unique_file_ids": args.unique_file_ids, 
        "batch_size": args.batch_size,
        "workers":  args.workers,
        "logger": logger
    }

    report = threading_run(**modes_parameters)

    return report


def start_multiprocessing_mode(args: argparse.Namespace) -> dict:
    db_url = create_db_url(args)

    modes_parameters = {
        "db_url": db_url,
        "rows": args.rows,
        "unique_file_ids": args.unique_file_ids, 
        "batch_size": args.batch_size,
        "workers":  args.workers,
        "log_file": args.log_file
    }

    report = multiprocessing_run(**modes_parameters)

    return report


def start_asyncio_mode(args: argparse.Namespace) -> dict:
    logger = setup(args.log_file)
    db_url = create_db_url(args)
    
    modes_parameters = {
        "db_url": db_url,
        "rows": args.rows,
        "unique_file_ids": args.unique_file_ids, 
        "batch_size": args.batch_size,
        "workers":  args.workers,
        "logger": logger
    }

    report = asyncio.run(asynco_run(**modes_parameters))

    return report


def main():
    MODES = {
        'single': start_single_mode,
        'threading': start_threading_mode,
        'multiprocessing': start_multiprocessing_mode,
        'asyncio': start_asyncio_mode
    }
    parser = create_parser()
    args = parser.parse_args()
    if not check_args_valid(args):
        return
    
    report = MODES[args.mode](args)
    save_results(report, args.results_file)


if __name__ == '__main__':
    main()