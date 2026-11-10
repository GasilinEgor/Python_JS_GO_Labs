import os
import psutil


def get_memory() -> float:
    process = psutil.Process(os.getpid())
    memory_bytes = process.memory_info().rss

    return memory_bytes / (1024 * 1024)