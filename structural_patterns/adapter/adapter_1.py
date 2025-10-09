""" Adapter Pattern 1

Scenario: Integrating a legacy rectangle API with a new interface
"""

# New expected interface
class Shape:
    def area(self) -> float:
        return 10

# Legacy class that we cannot change
class LegacyRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

# Adapter wraps a LegacyRect and exposes the expected interface
class RectAdapter(Shape):
    def __init__(self, legacy: LegacyRect):
        self.legacy = legacy
    
    def area(self) -> float:
        return self.legacy.get_area()
    
if __name__ == '__main__':
    legacy = LegacyRect(0, 0, 1 + 2, 1 + 3)
    shape = RectAdapter(legacy)
    print("Area: ", shape.area())