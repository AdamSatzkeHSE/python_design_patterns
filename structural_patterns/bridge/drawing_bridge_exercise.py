# Drawing app where shapes (abstractions) can be rendered by different renderers
# implementations without exploding a class count

# Goal
# Decouple what you draw: circle, rectangle, etc. from how you draw it (ASCII, SVG, JSON)
# You should be able to add new shapes or renderers independently

""" Solution:
- Abstraction heirarchy: Shape -> Circle Rectangle Line
- Implementation hierarchy: Renderer -> ASCIIRenderer, SVGRenderer, JSONRenderer
- Client code composes Shape(Renderer) at runtime and calls shape.draw()
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

class Renderer(ABC):
    @abstractmethod
    def render(self, shape):
        pass

class ASCIIRenderer(Renderer):
    def __init__(self, shape):
        self.shape = shape

    def render(self, shape) -> None:
        print(f"[ASCII Renderer]: Rendering shape {self.shape}")

class SVGRenderer(Renderer):
    def __init__(self, shape):
        self.shape = shape

    def render(self, shape):
        print(f"[SVG Renderer]: Rendering shape {self.shape}")

class JSONRenderer(Renderer):
    def __init__(self, shape):
        self.shape = shape

    def render(self, shape):
        print(f"[JSONRenderer] Rendering shape {self.shape}")

class Shape(ABC):
    renderer : Renderer

    @abstractmethod
    def draw(self) -> str:
        pass

class Circle(Shape):
    pass

class Rectangle(Shape):
    pass

class Line(Shape):
    pass

