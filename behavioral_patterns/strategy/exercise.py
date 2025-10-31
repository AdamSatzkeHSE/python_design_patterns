# Create a pluggable DiscountStrategy for a checkout.
# Implement NoDiscount, PercentOff(10%) and LoyaltyPoints(1 Euro per 100 pts)

# checkout(total, strategy) should return the final price.

class DiscountStrategy: ...
class NoDiscount(DiscountStrategy): ...
class PercentOff(DiscountStrategy): ...
class LoyaltyPoints(DiscountStrategy): ...

def checkout(total, strategy: DiscountStrategy):
    ...

# --- Try it ---
if __name__ == "__main__":
    print(checkout(100, NoDiscount()))
    print(checkout(200, PercentOff(10)))
    print(checkout(80, LoyaltyPoints(points=250)))

    