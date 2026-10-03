from shape import Shape

class Rectangle(Shape):
    def __init__(self, name, width=1, height=1):
        super().__init__(name)
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def square(self):
        return self.width * self.height
    
    def __str__(self):
        return f'{self.name}: длина = {self.width}, ширина = {self.height}'