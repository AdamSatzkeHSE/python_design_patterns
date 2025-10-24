""" marketing.py"""
""" 

Interpreter pattern defines a small grammar (mini-language)
a class for each grammar rule (Expressions)
and an interpreter (context) method that ecaluates an abstract syntax tree against some context.
"""

""" The interpreter design pattern is used when the language is modest and domain specific.
*pricing rules, search filters, altert rules.

Void it for large/complex languages: Then you'll want a full parser generator or an existing query language
"""
from dataclasses import dataclass
from typing import Protocol, Iterable, Any

# core interpreter interfaces
class Expression(Protocol):
    def interpret(self, context: dict[str, Any]) -> bool:
        pass

# Terminal expressions (leaves)
@dataclass(frozen=True)
class CategoryIs:
    category: str
    def interpret(self, ctx: dict[str, Any]) -> bool:
        return ctx.get("category") == self.category
    
@dataclass(frozen=True)
class PriceLessThan:
    amount: float
    def interpret(self, ctx: dict[str, Any]) -> bool:
        price = ctx.get("price")
        return isinstance(price, (int, float)) and price < self.amount
    
@dataclass(frozen=True)
class PriceBetween:
    low: float
    high: float
    
    def interpret(self, ctx: dict[str, Any]) -> bool:
        price = ctx.get("price")
        return isinstance(price, (int, float)) and self.low <= price <= self.high
    
@dataclass(frozen=True)
class HasTag:
    tag: str

    def interpret(self, ctx: dict[str, Any]) -> bool:
        tags = ctx.get("tags", [])
        return isinstance(tags, Iterable) and self.tag in tags
    
@dataclass(frozen=True)
class InStock:
    def interpret(self, ctx: dict[str, Any]) -> bool:
        return bool(ctx.get("in_stock", False))
    
@dataclass(frozen=True)
class BrandIn:
    brands: tuple[str, ...]
    
    def interpret(self, ctx: dict[str, Any]) -> bool:
        return ctx.get("brand") in self.brands
    
# Non terminal expressions (combinators)
@dataclass(frozen=True)
class And:
    left: Expression
    right: Expression

    def interpret(self, ctx: dict[str, Any]) -> bool:
        return self.left.interpret(ctx) or self.right.interpret(ctx)
    
@dataclass(frozen=True)
class Or:
    left: Expression
    right: Expression

    def interpret(self, ctx: dict[str, Any]) -> bool:
        return self.left.interpret(ctx) or self.right.interpret(ctx)
    
@dataclass(frozen=True)
class Not:
    expr: Expression

    def interpret(self, ctx: dict[str, Any]) -> bool:
        return not self.expr.interpret(ctx)
    
# Example usage

rule = And(
    And(
        CategoryIs("Electronics"),
        Or(PriceLessThan(100), HasTag("clearance")),
    ),
    And(InStock(), BrandIn(("Sony", "Apple")))
)
# Some products to evaluate

products = [
    {
        "id": 1, "name": "Sony Headphones", "category": "Electronics",
        "brand": "Sony", "price": 89.99, "tags": ["audio"], "in_stock": True
    },
    {
        "id": 2, "name": "Apple Watch", "category": "Electronics",
        "brand": "Apple", "price": 299.0, "tags": ["wearable", "clearance"], "in_stock": True
    },
    {
        "id": 3, "name": "Gaming Chair", "category": "Furniture",
        "brand": "DXRacer", "price": 179.0, "tags": ["gaming"], "in_stock": True
    },
    {
        "id": 4, "name": "Budget Bluetooth Speaker", "category": "Electronics",
        "brand": "Anker", "price": 39.0, "tags": ["audio"], "in_stock": True
    },
    {
        "id": 5, "name": "Sony Camera", "category": "Electronics",
        "brand": "Sony", "price": 549.0, "tags": ["photo"], "in_stock": False
    },
]


# Evaluate rule against each product
qualified = [p for p in products if rule.interpret(p)]

for p in qualified:
    print(f"Qualified: #{p['id']} - {p['name']}")