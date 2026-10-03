from timing import Timeit
from random import randint


def next_fib(a, b):
    return a + b

@Timeit
def fib_while(a, b, n):
    fib = [a, b]
    i = 2
    while i < n:
        c = next_fib(a, b)
        fib.append(c)
        a, b = b, c
        i += 1
    
    return fib

@Timeit
def fib_range(a, b, n):
    fib = [a, b]
    for i in range(2, n):
        c = next_fib(a, b)
        fib.append(c)
        a, b = b, c
    
    return fib

@Timeit
def fib_generator(a, b, n):
    i = 2
    while i < n:
        c = next_fib(a, b)
        yield c
        a, b = b, c

def main():
    res1 = fib_while(1, 1, 100)
    res4 = fib_while(1, 1, randint(10, 100))
    res5 = fib_while(1, 1, randint(10, 100))
    res2 = fib_range(1, 1, 100)
    res3 = fib_generator(1, 1, 100)
    print(fib_while.count())
    fib_while.report()


if __name__ == '__main__':
    main()