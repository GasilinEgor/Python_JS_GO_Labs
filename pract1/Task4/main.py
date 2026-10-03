from rectangle import Rectangle
from circle import Circle
from triangle import Triangle
from random import randint


def main():
    rectangle = Rectangle("Прямоугольник", randint(1, 100), randint(1, 100))
    print(rectangle)
    print(rectangle.square())

    a, b, c = randint(1, 100), randint(1, 100), randint(1, 100)
    while not((a + b > c) and (a + c > b) and (b + c > a)):
        a, b, c = randint(1, 100), randint(1, 100), randint(1, 100)
    triangle = Triangle("Треугольник", a, b, c)
    print(triangle)
    print(triangle.square())

    circle = Circle("Круг", randint(1, 100))
    print(circle)
    print(circle.square())


if __name__ == '__main__':
    main()