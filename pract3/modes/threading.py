import logging
from generator import generate_batch, generate_uuid
from model import GenerativeTable
from metrics import get_memory
from errors import ThreadWorkError

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
import uuid
import time
import threading


def split_work(rows_count: int, workers: int) -> list[tuple[int, int]]:
    clear_rows = rows_count // workers
    dirty_rows = rows_count % workers
    ranges = []

    start = 0
    for tworker_index in range(workers):
        end = start + clear_rows
        if dirty_rows > 0:
            end += 1
            dirty_rows -= 1
        
        ranges.append(end - start)
        start = end
    
    print(ranges)
    return ranges


logger = logging.getLogger(__name__)


def one_thread_work(engine: Engine, rows: int, batch_size: int, uuid_pool: list[uuid.UUID], logger: logging.Logger, worker_id: int, lock: threading.Lock, results: list[dict]) -> None:
    inserted_rows = 0
    batch_num = 0
    max_memory = get_memory()
    start = time.perf_counter()
    logger.info("Поток %s начинает работу", worker_id)
    try:
        with engine.begin() as connection:
            while inserted_rows < rows:
                cur_batch_size = min(batch_size, rows - inserted_rows)
                batch = generate_batch(cur_batch_size, uuid_pool)

                stmt = (insert(GenerativeTable).values(batch).on_conflict_do_nothing(index_elements=["field_id", "ip", "port"]).execution_options(preserve_rowcount=True))
                result = connection.execute(stmt)
                inserted = result.rowcount
                if inserted < 0:
                    inserted = 0
                
                inserted_rows += inserted
                batch_num += 1
                work_time = time.perf_counter() - start

                logger.info("[thread-%s] inserted batch %s (size=%s) at %s ms",
                worker_id, batch_num, cur_batch_size, work_time)

                with lock:
                    results.append({"inserted": inserted, "memory": get_memory(), "work_time": work_time})

    except Exception:
        logger.exception("На потоке %s произошла ошибка при вставке данных", worker_id)
        raise ThreadWorkError("Ошибка работы потока!")


def run(engine: Engine, rows: int, unique_file_ids: int, batch_size: int, workers: int, logger: logging.Logger) -> dict:
    uuid_pool = generate_uuid(unique_file_ids)
    threads = []
    results = []
    lock = threading.Lock()
    rows_per_worker = split_work(rows, workers)
    
    threads_start = time.perf_counter()
    threads_max_memory = get_memory()

    for workers_id in range(workers):
        work_parametrs = {
            "engine": engine,
            "rows": rows_per_worker[workers_id],
            "batch_size": batch_size,
            "uuid_pool": uuid_pool,
            "logger": logger,
            "worker_id": workers_id,
            "lock": lock,
            "results": results
        }

        thread = threading.Thread(target=one_thread_work, kwargs=work_parametrs)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    work_time =  time.perf_counter() - threads_start
    inserted_rows = sum((result["inserted"] for result in results))
    # max_memory = max((result["memory"] for result in results))
    max_memory = 0

    report = {
        "mode": "threading",
        "workers": workers,
        "inserted_rows": inserted_rows,
        "work_time": work_time,
        "peak_memory": max(max_memory, threads_max_memory)
    }

    return report


if __name__ == "__main__":
    rows_count = 101
    workers = 3
    split_work(rows_count, workers)        
