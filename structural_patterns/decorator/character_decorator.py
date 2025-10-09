""" Decorator pattern in gaming context:
power ups, speed boost, shield, damage must be added
without modifying the Player class
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import random

# Component interface
class Character(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def attack(self) -> int:
        pass

    @abstractmethod
    def take_damage(self, dmg: int) -> None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass

    @abstractmethod
    def stats(self) -> dict:
        pass

# Concrete component
@dataclass
class Player(Character):
    _name: str
    hp: int
    base_attack: int
    speed: int

    def name(self) -> str:
        return self._name
    
    def attack(self) -> int:
        roll = self.base_attack + random.randint(0, 3)
        return roll

    def take_damage(self, dmg: int) -> None:
        self.hp = max(0, self.hp - dmg)
    
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def stats(self) -> dict:
        return {"name": self._name, "hp": self.hp, "atk": self.base_attack, "spd": self.speed}

# Base decorator
class CharacterDecorator(Character):
    """ Base wrapper that forwards calls to the wrapped character """
    def __init__(self, inner: Character):
        self.inner = inner

    # Default: forward everything
    def name(self) -> str:
        return self.inner.name()

    def attack(self) -> int:
        return self.inner.attack()

    def take_damage(self, dmg: int) -> None:
        self.inner.take_damage(dmg)

    def is_alive(self) -> bool:
        return self.inner.is_alive()

    def stats(self) -> dict:
        return self.inner.stats()

# Concrete Decorators -> use the CharacterDecorator
class SpeedBoost(CharacterDecorator):
    """ +X speed for N turns """
    def __init__(self, inner: Character, bonus_spd: int, turns: int):
        super().__init__(inner)
        self.bonus_spd = bonus_spd
        self.turns = turns

    def stats(self) -> dict:
        s = self.inner.stats().copy()
        s["spd"] += self.bonus_spd
        s["buff_speed"] = f"+{self.bonus_spd} ({self.turns}t)"
        return s
    
class DamageBoost(CharacterDecorator):
    """ +% attack damage for N turns """
    def __init__(self, inner: Character, percent: float, turns: int):
        super().__init__(inner)
        self.percent = percent
        self.turns = turns
    
    def attack(self) -> int:
        base = self.inner.attack()
        boosted = int(round(base * (1 + self.percent)))
        return boosted
    
    def stats(self) -> dict:
        s = self.inner.stats().copy()
        s["buff_attack"] = f"+{int(self.percent * 100)}% ({self.turns}t)"
        return s
    
class Shield(CharacterDecorator):
    """ Reduce damage by flat amount of N turns. """
    def __init__(self, inner: Character, flat_reduction: int, turns: int):
        super().__init__(inner)
        self.flat = flat_reduction
        self.turns = turns

    def take_damage(self, dmg: int) -> None:
        mitigated = max(0, dmg - self.flat)
        self.inner.take_damage(mitigated)

    def stats(self) -> dict:
        s = self.inner.stats().copy()
        s["buff_shield"] = f"-{self.flat} dmg ({self.turns}t)"
        return s
    
# Utility: advance turns and drop expired decorators
def end_of_turn(char: Character):
    """ Walk down the decorator chain. If a decorator has 'turns',
    decrement and drop it when it hits zero.
    """
    # If it's not a decorator with turns, just return
    if not isinstance(char, CharacterDecorator):
        return char
    
    # first update inner layers
    inner = end_of_turn(char.inner) 
    # re-link in case inner changed
    char.inner = inner

    # If this decorator has a 'turns' attribute, tick it down.
    if hasattr(char, "turns"):
        char.turns -= 1
        if char.turns <= 0:
            # remove decorator, keep the inner
            return char.inner
    
    return char

if __name__ == "__main__":
    random.seed(1)
    hero: Character = Player("Aria", hp=50, base_attack=7, speed=5)
    print("Turn 0 - base stats:", hero.stats())

    # Pick up a speed boost (3 turns) and a shield (2 turns), then a damage boost (2 turns)
    hero = SpeedBoost(hero, bonus_spd=4, turns=3)
    hero = Shield(hero, flat_reduction=4, turns=2)
    hero = DamageBoost(hero, percent=0.5, turns=2)

    # Simulate a few turns
    for turn in range(1, 6):
        print(f"\n--- Turn {turn} ---")
        # Attack
        dmg = hero.attack()
        print(f"{hero.name()} attacks for {dmg} damage")

        # Take incoming damage (simulate enemy hit)
        incoming = 10 + random.randint(-2, 2)
        hero.take_damage(incoming)
        print(f"{hero.name()} takes {incoming} incoming. Post-mitigation HP: {hero.stats()["hp"]}")

        # Show stats
        print("Current stats:", hero.stats())
        
        # Advance time: decorators with turns tick down and expire
        hero = end_of_turn(hero)

        # Also a report after expiration
        print("After end of turn:", hero.stats())
        if not hero.is_alive():
            print(f"{hero.name()} is dead!")
            break