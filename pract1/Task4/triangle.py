from shape import Shape
from math import sqrt


class Triangle(Shape):
    def __init__(self, name, a=1, b=1, c=1):
        super().__init__(name)
        self._a = a
        self._b = b
        self._c = c
    
    @property
    def a(self):
        return self._a
    
    @property
    def b(self):
        return self._b
    
    @property
    def c(self):
        return self._c
    
    def square(self):
        p = (self.a + self.b + self.c) / 2
        return sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
    
    def __str__(self):
        return f'{self.name}: стороны: {self.a}, {self.b}, {self.c}'