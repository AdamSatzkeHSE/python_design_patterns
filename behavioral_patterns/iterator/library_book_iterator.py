# 🧩 Exercise: Library Book Iterator
# Goal:

# Implement an iterator that lets you iterate over the books in a library, even though the books are grouped by shelves.

# You’ll create:

# A Book class

# A Shelf class (which contains many Books)

# A Library class (which contains many Shelfs)

# A LibraryIterator that allows you to iterate through all books in the library, one by one.

# ✅ Step-by-step requirements

# Define a Book class with title and author attributes.

# Define a Shelf class that:

# Holds a list of Book objects.

# Is iterable (so you can loop over its books).

# Define a Library class that:

# Contains multiple Shelf objects.

# Returns a LibraryIterator when iter(library) is called.

# Implement a LibraryIterator class that:

# Iterates over all shelves and all books on each shelf.
from typing import List, Iterator

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

    def __repr__(self):
        return f"{self.title} by {self.author}"


class Shelf:
    def __init__(self):
        self._books: List[Book] = []

    def add_book(self, book: Book):
        self._books.append(book)

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)  # delegate iteration to the list


class LibraryIterator(Iterator[Book]):
    def __init__(self, shelves: List[Shelf]):
        self._shelves = shelves
        self._shelf_index = 0
        self._book_iter = iter(self._shelves[0]) if shelves else None

    def __iter__(self):
        return self

    def __next__(self) -> Book:
        if not self._shelves:
            raise StopIteration
        try:
            return next(self._book_iter)
        except StopIteration:
            self._shelf_index += 1
            if self._shelf_index >= len(self._shelves):
                raise StopIteration
            self._book_iter = iter(self._shelves[self._shelf_index])
            return next(self._book_iter)


class Library:
    def __init__(self):
        self._shelves: List[Shelf] = []

    def add_shelf(self, shelf: Shelf):
        self._shelves.append(shelf)

    def __iter__(self) -> LibraryIterator:
        return LibraryIterator(self._shelves)


# --- Demo ---
if __name__ == "__main__":
    # Create shelves
    shelf1 = Shelf()
    shelf1.add_book(Book("1984", "George Orwell"))
    shelf1.add_book(Book("Animal Farm", "George Orwell"))

    shelf2 = Shelf()
    shelf2.add_book(Book("The Hobbit", "J.R.R. Tolkien"))
    shelf2.add_book(Book("The Silmarillion", "J.R.R. Tolkien"))

    # Create library
    library = Library()
    library.add_shelf(shelf1)
    library.add_shelf(shelf2)

    print("Books in library:")
    for book in library:
        print("->", book)
