from logger import logging
from generator import generate_batch, generate_uuid
from model import GenerativeTable
from metrics import get_memory

from sqlalchemy import insert
from sqlalchemy.engine import Engine
import time


def run(engine: Engine, rows: int, unique_file_ids: int, batch_size: int, logger) -> dict:
    uuid_pool = generate_uuid(unique_count=unique_file_ids)
    inserted_rows = 0
    batch_num = 0
    max_memory = get_memory()
    start = time.perf_counter()

    with engine.begin() as connection:
        while inserted_rows < rows:
            cur_batch_size = min(batch_size, rows - inserted_rows)
            batch = generate_batch(cur_batch_size, uuid_pool)
            connection.execute(insert(GenerativeTable), batch)

            inserted_rows += cur_batch_size
            batch_num += 1
            cur_memory = get_memory()
            max_memory = max(max_memory, cur_memory)

            logger.info("[single] inserted batch %s (size=%s) at %s ms", batch_number, current_batch_size, time.perf_counter() - start)
        
        work_time = time.perf_counter() - start

    report = {
        "mode": "single",
        "workers": 1,
        "inserted_rows": inserted_rows,
        "work_time": work_time,
        "peak_memory": max_memory
    }
    
    return report
