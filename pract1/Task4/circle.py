from shape import Shape
from math import pi


class Circle(Shape):
    def __init__(self, name, radius = 1):
        super().__init__(name)
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    def square(self):
        return pi * self.radius ** 2
    
    def __str__(self):
        return f'{self.name}: радиус = {self.radius}'