from functools import update_wrapper
from time import perf_counter
from datetime import datetime
from dataclasses import dataclass

@dataclass
class FuncWorkLog:
    func_name: str
    args: list
    kwargs: dict
    res: Any
    work_time: float
    work_start: datetime

class Timeit:
    def __init__(self, fn):
        self._fn = fn
        self.history = []
        update_wrapper(self, fn)
    
    def __call__(self, *args, **kwargs):
        start = perf_counter()
        start_data = datetime.now().strftime("%d-%m-%Y %S:%M:%H")
        res = self._fn(*args, **kwargs)
        end = perf_counter()

        func_Log = FuncWorkLog(
            self._fn.__name__,
            args,
            kwargs,
            res,
            end - start,
            start_data,
            )
        
        self.history.append(func_Log)
        return res
    
    @staticmethod
    def get_log(log: FuncWorkLog):
        res = []
        res.append(f'Функция {log.func_name}')
        res.append(f'Парамтетры:\nargs = {log.args}\nkwargs={log.kwargs}') 
        res.append(f'Результат {log.res}')
        res.append(f'Начало: {log.work_start}')
        res.append(f'Время выполнения: {log.work_time}')
        return "\n".join(res)
    
    def last(self):
        last_log = self.history[-1]
        return self.get_log(last_log)
    
    def count(self):
        return len(self.history)
    
    def clear(self):
        self.history = []
    
    def report(self):
        for log in self.history:
            print(self.get_log(log))
            print('||||||||||||||||||||||||||||||||')