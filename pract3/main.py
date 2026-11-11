from parser import create_parser
from validation import check_args_valid

from modes.single import run as single_run


def create_db_url(args: argparse.Namespace) -> str:
    return f"postgresql://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}"


def save_results(report: dict, result_file: str) -> None:
    text = (
        f"Режим работы: {report["mode"]}\n"
        f"Количество потоков/процессов: {report['workers']}\n"
        f"Вставлено строк: {report["inserted_rows"]}\n"
        f"Время работы: {report["work_time"]}"
        f"Максимальные затраты памяти: {report["peak_memory"]}"
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
    MODES[args.mode]()


if __name__ == '__main__':
    main()