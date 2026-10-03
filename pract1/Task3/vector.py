from math import sqrt


class Vector:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __str__(self):
        return f'<{self.x}; {self.y}>'
    
    def __repr__(self):
        return f'<{self.x}; {self.y}>'
    
    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other: Vector):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other: Vector):
        return not(self == other)
    
    def __mul__(self, val):
        if isinstance(val , int):
            return Vector(self.x * val, self.y * val)
        elif isinstance(val, Vector):
            return self.x * val.x + self.y * val.y
        else:
            raise ValueError
    
    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def print(self):
        print(self)


def main():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    v1.print()


if __name__ == '__main__':
    main()
