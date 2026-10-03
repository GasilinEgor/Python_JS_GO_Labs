from vector import Vector
from random import randint


def main():
    v1 = Vector(randint(-100, 100), randint(-100, 100))
    v2 = Vector(randint(-100, 100), randint(-100, 100))
    num = randint(-100, 100)
    print("Начальные вектора:")
    print(v1)
    print(v2)
    print(f'Число для тестирования: {num}\n')
    print(f'Сумма векторов: {v1 + v2}')
    print(f'Разница векторов: {v1 - v2}')
    print(f'Равность векторов: {v1 == v2}')
    print(f'Неравность векторов: {v1 != v2}')
    print(f'Произведение на число: {v1 * num}')
    print(f'Произведение векторов: {v1 * v2}')
    print(f'Длина вектора: {abs(v1)}')
    print(f'Вывод вектора: {v1}')


if __name__ == '__main__':
    main()