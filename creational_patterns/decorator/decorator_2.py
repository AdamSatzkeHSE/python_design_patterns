""" The Decorator is a structural design pattern that lets you dynamically add new behavior
to objects without modifying their code.


Its like wrapping an object in layers, each adding extra functionality
"""

# When to use it:
# - When adding responsabilities dynamically to objects.
# - When subclassing would create too many combinations of features
# - When you want to follow open / closed principle: Open for extension, closed for modification


# Imagine a coffee shop:

# Base coffee = $5

# You can decorate it with milk, sugar, whipped cream, caramel, etc.
# Each “add-on” changes behavior (price, description) 
# but we don’t want a huge subclass explosion like MilkCoffee, SugarMilkCoffee, WhippedSugarMilkCoffee, etc.
# Decorator pattern solves this.

class Coffee:
    def cost(self) -> float:
        raise NotImplementedError
    
    def description(self) -> str:
        raise NotImplementedError
    
# Concrete component
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 5.0
    
    def description(self) -> str:
        return "Simple Coffee"
    
# Base decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()
    
# Concrete decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 1.5

    def description(self) -> str:
        return super().description() + "milk"
    
class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.5
    
    def description(self):
        return super().description() + "sugar"
    

if __name__ == '__main__':
    # Create a simple coffee
    coffee = SimpleCoffee()
    print(coffee.description(), "-> $", coffee.cost())

    # Add milk
    coffee = MilkDecorator(coffee)
    print(coffee.description(), "-> $", coffee.cost())

    # Add sugar
    coffee = SugarDecorator(coffee)
    print(coffee.description(), "-> $", coffee.cost())
    
    
