""" Composite Pattern
Scenario: File System tree: Folders contain files and subfolders
"""

from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def size(self) -> int:
        pass

class File(Node):
    def __init__(self, name, size):
        self.name = name
        self._size = size
    
    def size(self) -> int:
        return self._size

class Folder(Node):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, node: Node):
        self.children.append(node)

    def size(self) -> int:
        return sum(c.size() for c in self.children)
    

if __name__ == "__main__":
    root = Folder("root")
    root.add(File("a.txt", 11))
    sub = Folder("docs")
    sub.add(File("readme.md", 6))
    root.add(sub)
    print("Total size:", root.size())