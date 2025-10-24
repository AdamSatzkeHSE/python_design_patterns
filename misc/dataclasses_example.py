"""
tutorial_dataclasses.py

This tutorial demonstrates how to use Python's 'dataclasses' module
to simplify class definitions by automatically generating boilerplate
code such as __init__, __repr__, __eq__, and more.

The 'dataclasses' module was introduced in Python 3.7 and is especially
useful for classes that are mainly used to store data.

"""

# ------------------------------------------------------------
# 1. Basic usage of @dataclass
# ------------------------------------------------------------
from dataclasses import dataclass, field, asdict, astuple
from typing import List

@dataclass
class Person:
    """A simple data class representing a person."""

    name: str
    age: int
    city: str = "Unknown"  # Default value

# The @dataclass decorator automatically generates:
#   - __init__(self, name, age, city)
#   - __repr__ for pretty printing
#   - __eq__ for equality comparison


# ------------------------------------------------------------
# 2. Using default_factory for mutable types
# ------------------------------------------------------------
@dataclass
class Team:
    """Demonstrates default_factory for mutable fields."""

    name: str
    members: List[Person] = field(default_factory=list)

    def add_member(self, person: Person):
        self.members.append(person)


# ------------------------------------------------------------
# 3. Adding custom methods and computed fields
# ------------------------------------------------------------
@dataclass
class Rectangle:
    """A class with computed properties and methods."""

    width: float
    height: float

    @property
    def area(self) -> float:
        """Computed property that is not stored as a field."""
        return self.width * self.height

    def scale(self, factor: float):
        """Method that scales both dimensions."""
        self.width *= factor
        self.height *= factor


# ------------------------------------------------------------
# 4. Controlling dataclass behavior
# ------------------------------------------------------------
@dataclass(order=True, frozen=True)
class Product:
    """Example showing ordering and immutability."""

    price: float
    name: str

# - order=True: adds comparison methods (__lt__, __le__, etc.)
# - frozen=True: makes the instance immutable (fields cannot be reassigned)


# ------------------------------------------------------------
# 5. Demonstration
# ------------------------------------------------------------
if __name__ == "__main__":
    # --- Person example ---
    alice = Person("Alice", 30, "Paris")
    bob = Person("Bob", 25)
    print("People:")
    print(alice)
    print(bob)
    print(f"Alice == Bob? {alice == bob}\n")

    # --- Team example ---
    team = Team("Developers")
    team.add_member(alice)
    team.add_member(bob)
    print("Team:")
    print(team)
    print("Members:", team.members, "\n")

    # --- Rectangle example ---
    rect = Rectangle(5, 3)
    print("Rectangle:")
    print(f"Width: {rect.width}, Height: {rect.height}, Area: {rect.area}")
    rect.scale(2)
    print(f"After scaling: Width: {rect.width}, Height: {rect.height}, Area: {rect.area}\n")

    # --- Product example ---
    p1 = Product(19.99, "Book")
    p2 = Product(25.00, "Headphones")
    print("Products:")
    print(p1)
    print(p2)
    print(f"Is p1 cheaper than p2? {p1 < p2}\n")

    # --- Converting to dicts or tuples ---
    print("As dict:", asdict(alice))
    print("As tuple:", astuple(alice))

# ------------------------------------------------------------
# 6. Key Takeaways
# ------------------------------------------------------------
# Use @dataclass for classes that primarily store data.
# field(default_factory=...) is required for mutable defaults.
# frozen=True makes the object immutable.
# order=True automatically provides comparison methods.
# asdict() and astuple() convert dataclass instances easily.
# dataclasses.replace(obj, **changes) can create modified copies.
# ------------------------------------------------------------
