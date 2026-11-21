import os
import psutil


def get_memory() -> float:
    process = psutil.Process(os.getpid())
    memory_bytes = process.memory_info().rss

    return memory_bytes / (1024 * 1024)


def get_process_tree_memory() -> float:
    parent = psutil.Process(os.getpid())

    processes = [parent] + parent.children(recursive=True)

    total_memory = 0

    for process in processes:
        try:
            total_memory += process.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return total_memory / (1024 * 1024)