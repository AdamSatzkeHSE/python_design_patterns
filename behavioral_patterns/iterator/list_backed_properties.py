#
class Creature:
    def __init__(self, attack=0, defense=0, lp=0):
        # Explicit approach
        self.attack: int = attack
        self.defense: int = defense
        self.lp: int = lp

        # property list approach
        self.stats = [10, 10, 10]

    @property
    def sum_of_stats(self):
        return self.attack + self.defense + self.lp
    
    @property
    def strength(self):
        return self.attack + self.defense
    
    @property
    def max_stat(self):
        return max([self.attack, self.defense, self.lp])
        # retrun max(self.stats)