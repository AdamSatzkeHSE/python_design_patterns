""" We are building a game that spawns enemies. 
The rest of your code should not care which concrete class it gets
Only that it can call common methods like attack() and hp.
A factory decides what to create based on inputs like level/biome/difficulty
"""

# Simple factory: pick one enemy type
from abc import ABC, abstractmethod
import random

# Target interface (what the game code expects)
class Enemy(ABC):
    def __init__(self, name: str, hp: int, attack: int):
        self.name = name
        self.hp = hp
        self.atk = attack

    @abstractmethod
    def attack(self) -> int:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} hp={self.hp} attack={self.atk}"

# Concrete enemies (implementation detail)
class Slime(Enemy):
    def attack(self) -> int:
        # weak, small variance
        return max(1, self.atk + random.randint(-1, 1))
    
class Goblin(Enemy):
    def attack(self) -> int:
        # quick stab, medium variance
        return max(1, self.atk + random.randint(-2, 3))
    
class Dragon(Enemy):
    def attack(self) -> int:
        # breath attack, high variance
        base = self.atk + random.randint(-5, 10)
        # crit chance
        if random.random() < 0.15:
            base = int(base * 1.5)
        return max(5, base)
    
# Simple factory
class EnemyFactory:
    """ Chooses the concrete Enemy class and sclaes stats based on the level. """
    @staticmethod
    def create(enemy_type: str, level: int) -> Enemy:
        enemy_type = enemy_type.lower()

        # Simple stat scaling rules
        hp_scale = 10 + level * 3
        attack_scale = 3 + level // 2

        if enemy_type == "slime":
            return Slime("Slime", hp_scale, attack_scale)
        elif enemy_type == "goblin":
            return Goblin("Goblin", int(hp_scale * 1.2), attack_scale + 1)
        elif enemy_type == "dragon":
            return Dragon("Dragon", int(hp_scale), attack_scale + 6)
        else:
            raise ValueError(f"Unknown enemy_type: {enemy_type}")

# Client Code (game system)
def spawn_wave(types, level):
    enemies = [EnemyFactory.create(t, level) for t in types]
    print("Spawned wave:", enemies)
    damage = sum(e.attack() for e in enemies)
    print("Combined enemy attack this turn:", damage)

spawn_wave(["slime", "goblin", "dragon"], level=7)