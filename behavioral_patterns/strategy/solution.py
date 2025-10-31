class DiscountStrategy:
    def apply(self, total): 
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total): 
        return total

class PercentOff(DiscountStrategy):
    def __init__(self, percent): 
        self.percent = percent
    
    def apply(self, total): 
        return total * (1 - self.percent/100.0)

class LoyaltyPoints(DiscountStrategy):
    def __init__(self, points): 
        self.points = points
    def apply(self, total): 
        return max(0, total - (self.points // 100))

def checkout(total, strategy: DiscountStrategy):
    return round(strategy.apply(total), 2)

if __name__ == "__main__":
    print(checkout(100, NoDiscount()))
    print(checkout(200, PercentOff(10)))
    print(checkout(80, LoyaltyPoints(points=250)))