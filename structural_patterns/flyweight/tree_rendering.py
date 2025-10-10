from dataclasses import dataclass
from typing import Dict, Tuple
from weakref import WeakValueDictionary

# ---------- Flyweight (intrinsic state) ----------
@dataclass(frozen=True, slots=True)
class TreeType:
    name: str
    color: str
    texture_id: str   # pretend this identifies a big texture blob on disk/GPU

    def draw(self, x: int, y: int, height: int) -> None:
        # 'x, y, height' are EXTRINSIC; they vary per tree instance
        print(f"Drawing {self.name} at ({x},{y}) h={height} with color={self.color}, tex={self.texture_id}")

# ---------- Flyweight Factory ----------
class TreeTypeFactory:
    """
    Returns shared TreeType instances keyed by (name, color, texture_id).
    WeakValueDictionary lets GC collect unused flyweights.
    """
    _cache: "WeakValueDictionary[Tuple[str, str, str], TreeType]" = WeakValueDictionary()

    @classmethod
    def get(cls, name: str, color: str, texture_id: str) -> TreeType:
        key = (name, color, texture_id)
        tree_type = cls._cache.get(key)
        if tree_type is None:
            tree_type = TreeType(name, color, texture_id)
            cls._cache[key] = tree_type
        return tree_type

    @classmethod
    def unique_count(cls) -> int:
        return len(cls._cache)

# ---------- Context objects (hold extrinsic state) ----------
@dataclass(slots=True)
class Tree:
    x: int
    y: int
    height: int
    type: TreeType  # shared flyweight

    def draw(self) -> None:
        # delegate drawing to the shared flyweight, passing extrinsic state
        self.type.draw(self.x, self.y, self.height)

# ---------- Client that builds many trees ----------
class Forest:
    def __init__(self):
        self._trees: list[Tree] = []

    def plant_tree(self, x: int, y: int, height: int, name: str, color: str, texture_id: str):
        tree_type = TreeTypeFactory.get(name, color, texture_id)  # shared
        self._trees.append(Tree(x, y, height, tree_type))         # tiny per-tree

    def draw(self):
        for t in self._trees:
            t.draw()

if __name__ == "__main__":
    forest = Forest()

    # Plant thousands of trees that share just a few appearances
    for i in range(5000):
        forest.plant_tree(x=i % 500, y=i // 500, height=8,  name="Oak",   color="green", texture_id="oak_tex")
        forest.plant_tree(x=i % 500, y=i // 500, height=10, name="Pine",  color="dark",  texture_id="pine_tex")
        forest.plant_tree(x=i % 500, y=i // 500, height=6,  name="Birch", color="light", texture_id="birch_tex")

    # We planted 15,000 Tree objects, but only 3 shared TreeType flyweights:
    print("Trees:", len(forest._trees))
    print("Unique TreeTypes (flyweights):", TreeTypeFactory.unique_count())

    # Draw a sample
    for t in forest._trees[:3]:
        t.draw()