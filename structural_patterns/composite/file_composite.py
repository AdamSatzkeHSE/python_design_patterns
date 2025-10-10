""" The Composite pattern lets you treat individual objects and groups of objects
in the same way

You build tree-like structures of objects, where:
- Leaf nodes are individual items
- Composite nodes are collections of items
"""

""" File System
- a file is a leaf - it can't contain anything
- a folder is a composite - it can contain files and other folders
- you can perdorm operations like get_size() or show() on both, the same way.
"""

from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    """ Base Class for both files and folders."""
    @abstractmethod
    def show_details(self, indent=0):
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

# This is the Leaf
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def show_details(self, indent=0):
        print(" " * indent + f"- File: {self.name} ({self.size} KB)")

    def get_size(self):
        return self.size
    
# This is the Composite
class Folder(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)
    
    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def show_details(self, indent=0):
        print(" " * indent + f"+ Folder: {self.name}")
        for child in self.children:
            child.show_details(indent + 4)

    def get_size(self):
        return sum(child.get_size() for child in self.children)
    
# Now the folder can contain other components (files or foldersw) and
# delegate operations to them recursively.

if __name__ == "__main__":
    # Create files
    file1 = File("resume.pdf", 120)
    file2 = File("photo.png", 250)
    file3 = File("song.mp3", 5000)

    # Create folders
    downloads = Folder("Downloads")
    music = Folder("Music")
    documents = Folder("Documents")

    # Build Hierarchy
    downloads.add(file1)
    downloads.add(file2)
    music.add(file3)
    documents.add(downloads)
    documents.add(music)

    # Display structure
    documents.show_details()

    # Show total size
    print(f"Total Size: {documents.get_size()} KB")

""" real life use-cases
- File Systems
- company structures
- GUI Components
- Menues
- Organizational Charts
- Nested JSON or XML trees"""