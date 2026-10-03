from time import perf_counter
from functools import wraps


def timeit(func):
    @wraps(func)
    def timer(*args, **kwags):
        start = perf_counter()
        res = func(*args, **kwags)
        end = perf_counter()
        print(f'Функция {func.__name__} сработала за {(end - start) * 1000} секунд')
        return res
    
    return timer


def next_fib(a, b):
    return a + b

@timeit
def fib_while(a, b, n):
    fib = [a, b]
    i = 2
    while i < n:
        c = next_fib(a, b)
        fib.append(c)
        a, b = b, c
        i += 1
    
    return fib

@timeit
def fib_range(a, b, n):
    fib = [a, b]
    for i in range(2, n):
        c = next_fib(a, b)
        fib.append(c)
        a, b = b, c
    
    return fib

@timeit
def fib_generator(a, b, n):
    i = 2
    while i < n:
        c = next_fib(a, b)
        yield c
        a, b = b, c

def main():
    res1 = fib_while(1, 1, 100)
    res2 = fib_range(1, 1, 100)
    res3 = fib_generator(1, 1, 100)


if __name__ == '__main__':
    main()