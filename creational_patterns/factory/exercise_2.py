# Create a factory that can produce different types of shapes (Circle, Square, etc.) depending on input

from abc import ABC, abstractmethod


# 1. Create a common interface
class Shape(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

# 2. Implement concrete classes
class Circle(Shape):
    def draw(self):
        print("Drawing a Circle")

class Square(Shape):
    def draw(self):
        print("Drawing a Square")

# 3. Factory class
class ShapeFactory:
    def get_shape(self, shape_type: str) -> Shape:
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        
        else:
            raise ValueError("Unknown Shape")

if __name__ == "__main__":
    factory = ShapeFactory()
    shape = factory.get_shape("circle")
    shape.draw()