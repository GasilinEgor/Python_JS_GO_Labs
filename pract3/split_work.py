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
    
    return ranges