# In duck typing, Python doesn’t care what an object is — it only cares what it can do.
# If an object implements the required methods or behaviors, it can be used regardless of its class or inheritance.

class Duck:
    def quack(self):
        print("Quack, quack!")

class Person:
    def quack(self):
        print("I'm pretending to be a duck!")

def make_it_quack(thing):
    thing.quack()  # No type checking — just expects quack() to exist

duck = Duck()
person = Person()

make_it_quack(duck)     # Output: Quack, quack!
make_it_quack(person)   # Output: I'm pretending to be a duck!

# ✅ Advantages:

# Flexibility: Promotes polymorphism without rigid inheritance hierarchies.

# Less boilerplate: You don’t need to check types explicitly.

# Fits Python’s dynamic nature.

# ⚠️ Disadvantages:

# Potential runtime errors: If an object doesn’t implement the expected behavior, you’ll get an AttributeError at runtime.

# Less explicit: Harder to know what types are expected without documentation or type hints.
