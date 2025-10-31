""" Strategy lets you swap an algorithm at runtime without changing the code that uses it.
Instead of long if/else chaings, you encapsulate each algorithm behind a common interface
"""

# Use cases:
# Choosing a payment method
# shipping rates
# selecting a discount/tax rule
# picking a compression/sort algorithm


# What we want to avoid:
def shipping_cost(method, weight_kg):
    if method == "standard":
        return 3.50 + 1.0 * weight_kg
    elif method == "express":
        return 8.00 + 2.0 * weight_kg
    elif method == "pickup":
        return 0.0
    else:
        raise ValueError("Unknown method")
    
# Strategy with classes: 
from typing import Protocol
from dataclasses import dataclass

class ShippingStrategy(Protocol):
    def cost(self, weight_kg: float) -> float:
        pass


# 2) Concrete strategies
@dataclass
class StandardShipping:
    base: float = 3.50
    rate_per_kg: float = 1.0
    def cost(self, weight_kg: float) -> float:
        return self.base + self.rate_per_kg * weight_kg
    
@dataclass
class ExpressShipping:
    base: float = 8.00
    rate_per_kg: float = 2.0
    def cost(self, weight_kg: float) -> float:
        return self.base + self.rate_per_kg * weight_kg

class PickupShipping:
    def cost(self, weight_kg: float) -> float:
        return 0.0

# 3) Context: uses any ShippingStrategy
@dataclass
class Checkout:
    shipping: ShippingStrategy  # injected strategy
    items_total: float          # subtotal for items

    def total(self, weight_kg: float) -> float:
        return round(self.items_total + self.shipping.cost(weight_kg), 2)

if __name__ == "__main__":
    weight = 2.3  # kg
    cart_total = 49.99

    standard = Checkout(StandardShipping(), cart_total)
    express  = Checkout(ExpressShipping(),  cart_total)
    pickup   = Checkout(PickupShipping(),   cart_total)

    print("Standard:", standard.total(weight))  # e.g., 49.99 + (3.5 + 1.0*2.3)
    print("Express :", express.total(weight))   # e.g., 49.99 + (8.0 + 2.0*2.3)
    print("Pickup  :", pickup.total(weight))    # 49.99 + 0.0

    # Picking a strategy at runtime
    strategies = {
        "standard": StandardShipping,
        "express": ExpressShipping,
        "pickup": PickupShipping,
    }

    def make_shipping(method_name: str) -> ShippingStrategy:
        return strategies[method_name.lower()]()
    
    strategy = input("Choose a strategy: ")
    checkout = Checkout(make_shipping(strategy), items_total=79.0)
    print(checkout.total(weight_kg=5))