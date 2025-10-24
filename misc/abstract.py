"""
tutorial_abc_module.py

This tutorial demonstrates how to use Python's built-in 'abc' module to define and work
with Abstract Base Classes (ABCs).

The 'abc' module allows you to define abstract classes and methods that cannot
be instantiated directly and must be implemented by subclasses.
"""

# Importing necessary classes from abc
from abc import ABC, abstractmethod

# ------------------------------------------------------------
# 1. Defining an Abstract Base Class
# ------------------------------------------------------------
# The 'ABC' class is used as a base class for defining abstract classes.
# Methods decorated with @abstractmethod must be overridden by subclasses.

class Shape(ABC):
    """Abstract base class representing a geometric shape."""

    @abstractmethod
    def area(self):
        """Compute the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self):
        """Compute the perimeter of the shape."""
        pass

    def describe(self):
        """Concrete method: can be inherited as-is."""
        return f"This is a {self.__class__.__name__}."


# ------------------------------------------------------------
# 2. Implementing Concrete Subclasses
# ------------------------------------------------------------
# Subclasses must implement *all* abstract methods to be instantiable.

class Rectangle(Shape):
    """Concrete class implementing Shape for rectangles."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """Concrete class implementing Shape for circles."""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        from math import pi
        return pi * (self.radius ** 2)

    def perimeter(self):
        from math import pi
        return 2 * pi * self.radius


# ------------------------------------------------------------
# 3. Demonstrating Usage
# ------------------------------------------------------------
if __name__ == "__main__":
    # shape = Shape()  # ❌ This will raise an error: Can't instantiate abstract class
    # Uncommenting the above line will raise:
    # TypeError: Can't instantiate abstract class Shape with abstract methods area, perimeter

    rect = Rectangle(5, 3)
    circ = Circle(4)

    print(rect.describe())
    print(f"Rectangle area: {rect.area()}")
    print(f"Rectangle perimeter: {rect.perimeter()}\n")

    print(circ.describe())
    print(f"Circle area: {circ.area():.2f}")
    print(f"Circle perimeter: {circ.perimeter():.2f}\n")

    # Output example:
    # This is a Rectangle.
    # Rectangle area: 15
    # Rectangle perimeter: 16
    #
    # This is a Circle.
    # Circle area: 50.27
    # Circle perimeter: 25.13


# ------------------------------------------------------------
# 4. Key Takeaways
# ------------------------------------------------------------
# - Abstract classes cannot be instantiated directly.
# - Subclasses must implement all abstract methods.
# - Abstract classes can include concrete methods as well.
# - You can use isinstance() and issubclass() to check ABC relationships.
#
# Example:
# >>> isinstance(rect, Shape)
# True
# >>> issubclass(Rectangle, Shape)
# True
# ------------------------------------------------------------
