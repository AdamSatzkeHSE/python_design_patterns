from enum import Enum

# BEFORE
class Point:
    # Initialize with coordinate system
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Initialize with polar coordinates
    # def __init__...

    def __init__(self, a, b, system="CoordinateSystem"):
        ...
        if system == "Coordinate...":
            pass
        elif system == "CoordinatePolar...":
            pass

import math as m

# AFTER
class PointFactory:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y)
    
    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho * m.cos(theta), rho * m.sin(theta))