
import asyncio
import time

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.dialects.postgresql import insert

from logger import logging
from generator import generate_batch, generate_uuid
from model import GenerativeTable
from metrics import get_memory
from split_work import split_work


def change_url(db_url: str) -> str:
    db_url = db_url.replace("postgresql", "postgresql+asyncpg")
    return db_url


async def insert_worker(engine: AsyncEngine, rows: int, batch_size: int, uuid_pool: list, worker_id: int, logger: logging.Logger) -> dict:
    inserted_rows = 0
    batch_num = 0
    start_process = time.perf_counter()

    max_memory = get_memory()
    logger.info("Процесс %s начинает работу", worker_id)
    try:
        async with engine.begin() as connection:
            while inserted_rows < rows:
                cur_batch_size = min(batch_size, rows - inserted_rows)

                batch = generate_batch(cur_batch_size, uuid_pool)

                stmt = (insert(GenerativeTable).values(batch).on_conflict_do_nothing(index_elements=["field_id", "ip", "port"]).execution_options(preserve_rowcount=True))
                result = await connection.execute(stmt)
                inserted = result.rowcount
                if inserted < 0:
                    inserted = 0

                inserted_rows += inserted
                batch_num += 1
                work_time = time.perf_counter() - start_process

                current_memory = get_memory()
                max_memory = max(max_memory,current_memory)

                logger.info("[asyncio:%s] batch=%s size=%s ""inserted=%s time=%s ms",
                    worker_id, batch_num, cur_batch_size,inserted, work_time)
        work_time = time.perf_counter() - start_process

        return {
            "worker_id": worker_id,
            "inserted_rows": inserted_rows,
            "peak_memory": max_memory,
            "work_time": work_time,
            "error": None,
        }

    except Exception as err:
        logger.exception("[asyncio:%s] Ошибка при вставке данных", worker_id)

        return {
            "worker_id": worker_id,
            "inserted_rows": inserted_rows,
            "peak_memory": max_memory,
            "work_time": time.perf_counter() - start_worker,
            "error": str(err),
        }


async def run(db_url: str, rows: int, unique_file_ids: int, batch_size: int, workers: int, logger: logging.Logger) -> dict:
    uuid_pool = generate_uuid(unique_count=unique_file_ids)
    rows_per_worker = split_work(rows, workers)
    start = time.perf_counter()
    initial_memory = get_memory()

    db_url = change_url(db_url)
    print(db_url)
    engine = create_async_engine(db_url, pool_size=workers, max_overflow=0)

    try:
        tasks = []

        for worker_id, worker_rows in enumerate(rows_per_worker):
            work_parametrs = {
                    "engine": engine,
                    "rows": worker_rows,
                    "batch_size": batch_size,
                    "uuid_pool": uuid_pool,
                    "worker_id": worker_id,
                    "logger": logger
                }
            task = asyncio.create_task(insert_worker(**work_parametrs))
            tasks.append(task)
        worker_results = await asyncio.gather(*tasks)
    finally:
        await engine.dispose()
    work_time = time.perf_counter() - start

    errors = [result for result in worker_results if result["error"] is not None]

    if errors:
        raise RuntimeError(
            f"Ошибка в задаче {errors[0]['worker_id']}: "
            f"{errors[0]['error']}"
        )

    inserted_rows = sum(result["inserted_rows"] for result in worker_results)

    max_memory = max([initial_memory] + [result["peak_memory"] for result in worker_results])

    report = {
        "mode": "asyncio",
        "workers": workers,
        "inserted_rows": inserted_rows,
        "work_time": work_time,
        "peak_memory": max_memory,
    }

    return report
