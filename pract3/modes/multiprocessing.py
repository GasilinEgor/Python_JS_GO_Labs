import multiprocessing
import time

from logger import logging, setup_worker
from logging.handlers import QueueListener
from generator import generate_batch, generate_uuid
from model import GenerativeTable, make_db_engine
from metrics import get_memory, get_process_tree_memory
from split_work import split_work


from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

import psutil
import os


def insert_worker(db_url: str, rows: int, batch_size: int, uuid_pool: list, worker_id: int, results: multiprocessing.Queue, log_queue) -> None:
    logger = setup_worker(log_queue)
    logger.getEffectiveLevel()
    engine: Engine = make_db_engine(db_url)
    inserted_rows = 0
    batch_num = 0
    max_memory = get_memory()
    start_process = time.perf_counter()
    logger.info("Процесс %s начинает работу", worker_id)
    try:
        with engine.begin() as connection:
            while inserted_rows < rows:
                start_batch_time = time.perf_counter()
                cur_batch_size = min(batch_size, rows - inserted_rows)
                batch = generate_batch(cur_batch_size, uuid_pool)

                stmt = (insert(GenerativeTable).values(batch).on_conflict_do_nothing(index_elements=["field_id", "ip", "port"]).execution_options(preserve_rowcount=True))
                result = connection.execute(stmt)
                inserted = result.rowcount

                if inserted < 0:
                    inserted = 0

                inserted_rows += inserted
                batch_num += 1
                work_time = time.perf_counter() - start_batch_time

                current_memory = get_memory()
                max_memory = max(max_memory, current_memory)

                logger.info("[multiprocessing:%s] processed batch %s (size=%s, inserted=%s) at %s s",
                    worker_id, batch_num, cur_batch_size, inserted, time.perf_counter() - start_batch_time)

        results.put(
            {
                "worker_id": worker_id,
                "inserted_rows": inserted_rows,
                "peak_memory": max_memory,
                "work_time": work_time,
                "error": None,
            }
        )

    except Exception as err:
        logger.exception("[multiprocessing:%s] Ошибка при вставке данных", worker_id)
        results.put(
            {
                "worker_id": worker_id,
                "inserted_rows": inserted_rows,
                "peak_memory": max_memory,
                "error": str(err),
            }
        )

    finally:
        engine.dispose()


def run(db_url: str, rows: int, unique_file_ids: int, batch_size: int, workers: int, log_file: str) -> dict:
    uuid_pool = generate_uuid(unique_count=unique_file_ids)
    start = time.perf_counter()
    initial_memory = get_memory()
    results = multiprocessing.Queue()
    processes = []
    rows_per_worker = split_work(rows, workers)

    log_queue = multiprocessing.Queue()
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    listener = QueueListener(log_queue, file_handler, console_handler)
    listener.start()
    
    for worker_id in range(workers):
        worker_rows = rows_per_worker[worker_id]
        worker_parametrs = {
                "db_url": db_url,
                "rows": worker_rows,
                "batch_size": batch_size,
                "uuid_pool": uuid_pool,
                "worker_id": worker_id,
                "results": results,
                "log_queue": log_queue
            }
        process = multiprocessing.Process(target=insert_worker, kwargs=worker_parametrs)

        processes.append(process)
        process.start()

    worker_results = []

    max_memory = initial_memory
    parent = psutil.Process(os.getpid())

    while any(process.is_alive() for process in processes):
        current_memory = get_process_tree_memory()
        max_memory = max(max_memory, current_memory)

        time.sleep(0.05)

    max_memory = max(max_memory, get_process_tree_memory())

    for process in processes:
        process.join()

    for _ in processes:
        worker_results.append(results.get())

    work_time = time.perf_counter() - start

    errors = [result for result in worker_results if result["error"] is not None]

    if errors:
        raise RuntimeError(
            f"Ошибка в процессе {errors[0]['worker_id']}: "
            f"{errors[0]['error']}"
        )

    inserted_rows = sum(result["inserted_rows"] for result in worker_results)

    report = {
        "mode": "multiprocessing",
        "workers": workers,
        "inserted_rows": inserted_rows,
        "work_time": work_time,
        "peak_memory": max_memory,
    }

    return report