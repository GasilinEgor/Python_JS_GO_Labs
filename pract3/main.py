from parser import create_parser
from validation import check_args_valid
from model import make_db_engine
from logger import setup

import argparse

from modes.single import run as single_run




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
        f"Максимальные затраты памяти: {report["peak_memory"]} мб"
    )

    print(text)

    with open(result_file, "a", encoding='utf-8') as file:
        file.write(text)
        file.write("\n")


def main():
    MODES = {
        'single': single_run
    }
    parser = create_parser()
    args = parser.parse_args()
    if not check_args_valid(args):
        return

    db_url = create_db_url(args)
    engine = make_db_engine(db_url)

    logger = setup(args.log_file)
    report = MODES[args.mode](
        engine=engine, 
        rows=args.rows, 
        unique_file_ids=args.unique_file_ids, 
        batch_size=args.batch_size, 
        logger=logger
        )

    save_results(report, args.results_file)


if __name__ == '__main__':
    main()