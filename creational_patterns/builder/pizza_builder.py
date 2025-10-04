""" PizzaBuilder: Exposes chainable methods
build(): validates and returns the finished object.
PizzaDirector: Shows how to encode common builds """

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class Pizza:
    size: str
    crust: str
    sauce: str
    cheese: bool
    toppings: List[str] = field(default_factory=list)

class PizzaBuilder:
    def __init__(self) -> None:
        # sensible defaults
        self._size : Optional[str] = None
        self._crust: str = "classic"
        self._sauce: str = "tomato"
        self._cheese: bool = True
        self._toppings: List[str] = []

    def with_size(self, size: str) -> "PizzaBuilder":
        if size not in {"small", "medium", "large"}:
            raise ValueError("Size must be small, medium or large")
        self._size = size
        return self

    def with_sauce(self, sauce: str) -> "PizzaBuilder":
        self._sauce = sauce
        return self

    # chainable methods
    def with_crust(self, crust: str) -> "PizzaBuilder":
        self._crust = crust
        return self
    
    def with_cheese(self, cheese: bool) -> "PizzaBuilder":
        self._cheese = cheese
        return self
    
    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._topping.append(topping)
        return self
    
    def build(self) -> Pizza:
        # central place for validation
        if self._size is None:
            raise ValueError("size is required")
        
        if len(self._toppings) > 6:
            raise ValueError("too many toppings (max 6)")
        
        return Pizza(
            size=self._size,
            crust=self._crust,
            sauce=self._sauce,
            cheese=self._cheese,
            toppings=list(self._toppings)
        )
    
class PizzaDirector:
    """ Optional: predefined build sequences (pizza recipes)"""
    @staticmethod
    def marguerita() -> Pizza:
        return (PizzaBuilder().with_size("medium").with_crust("thin").with_sauce("tomato").with_cheese(True).build())

    @staticmethod
    def meat_lovers(size: str = "large") -> Pizza:
        return (PizzaBuilder().with_size(size).add_topping("pepperoni").add_topping("sausage").build())
    
if __name__ == '__main__':
    custom = (PizzaBuilder().with_size("large").with_crust("stuffed").with_sauce("pesto").build())
    preset = PizzaDirector.marguerita()

    print(custom)
    print(preset)