"""
tutorial_iterator_pattern.py

A practical tutorial on Python's Iterator Pattern.

What you'll learn:
1) The iterator protocol: __iter__ and __next__, StopIteration
2) Designing a proper Iterable vs. Iterator (and why it matters)
3) Generators: the easiest way to build iterators
4) Built-ins: iter(callable, sentinel), next(..., default), reversed()
5) itertools for powerful lazy pipelines
6) Best practices & common pitfalls

"""

from __future__ import annotations
from typing import Iterable, Iterator, TypeVar, Generic, Callable, Optional, Any, List, Tuple
from itertools import islice, takewhile, chain, groupby, count

T = TypeVar("T")

# ------------------------------------------------------------
# 1) The iterator protocol
# ------------------------------------------------------------
# - An *iterator* implements:
#     __iter__(self) -> Iterator[T]: returns self
#     __next__(self) -> T: returns the next item or raises StopIteration
# - An *iterable* simply defines __iter__ that returns a *new* iterator
#   each time it's called.
#
# The for-loop roughly does:
#   it = iter(obj)
#   while True:
#       try: x = next(it)
#       except StopIteration: break
#       <use x>


class Counter(Iterator[int]):
    """A simple finite iterator that counts from start (inclusive) to stop (exclusive)."""

    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> "Counter":
        # Iterators return themselves
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


# ------------------------------------------------------------
# 2) Iterable vs. Iterator: getting fresh iterators
# ------------------------------------------------------------
# IMPORTANT: If your object will be iterated multiple times (e.g., by different
# consumers or nested loops), implement an *Iterable* that creates a *new iterator*
# on each __iter__() call.
#
# Below, MyRange is an Iterable that returns a new _MyRangeIter iterator every time.


class _MyRangeIter(Iterator[int]):
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> "_MyRangeIter":
        return self

    def __next__(self) -> int:
        if (self.step > 0 and self.current >= self.stop) or (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


class MyRange(Iterable[int]):
    """Range-like iterable that yields numbers lazily."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("step cannot be 0")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> Iterator[int]:
        # Return a NEW iterator each time
        return _MyRangeIter(self.start, self.stop, self.step)


# ------------------------------------------------------------
# 3) Generators: the easiest iterators
# ------------------------------------------------------------
# A function using `yield` automatically implements the iterator protocol.
# You can also compose generators with `yield from`.

def fibonacci() -> Iterator[int]:
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def evens_up_to(n: int) -> Iterator[int]:
    """Finite generator yielding even numbers up to n (inclusive)."""
    for x in range(0, n + 1, 2):
        yield x


def composed_pipeline(n: int) -> Iterator[int]:
    """Compose two generators using `yield from`."""
    # Here we just delegate to evens_up_to; in real code you might chain multiple stages.
    yield from evens_up_to(n)


# ------------------------------------------------------------
# 4) Built-ins: iter(), next(), reversed(), __reversed__
# ------------------------------------------------------------
# - iter(obj)         -> gets an iterator from an iterable (calls obj.__iter__)
# - iter(callable, sentinel) -> repeatedly calls callable() until it returns sentinel
# - next(it, default) -> safe fetching (no StopIteration)
# - reversed(obj)     -> uses obj.__reversed__() if available; otherwise requires
#                        __len__ and __getitem__ (sequence protocol).


class LogFileLines(Iterable[str]):
    """An Iterable with a custom __reversed__ to iterate lines from the end.

    NOTE: This is a toy example that stores lines in memory. Real files are
    not efficiently reversible without indexing.
    """

    def __init__(self, lines: List[str]) -> None:
        self._lines = lines

    def __iter__(self) -> Iterator[str]:
        return iter(self._lines)  # delegate to list iterator

    def __reversed__(self) -> Iterator[str]:
        # Provide efficient reverse iteration
        return reversed(self._lines)


def iter_callable_demo() -> List[int]:
    """Use iter(callable, sentinel) to read until a sentinel value appears."""
    data = [1, 2, 3, 0, 4, 5]  # imagine these come from a sensor; 0 means 'stop'
    it = iter(data)            # basic iterator over the list

    def read() -> int:
        # Return next item or 0 if exhausted
        return next(it, 0)

    # Keep calling read() until it returns 0 (the sentinel)
    return list(iter(read, 0))


# ------------------------------------------------------------
# 5) itertools: building lazy pipelines
# ------------------------------------------------------------
# itertools gives you fast, memory-efficient building blocks.

def top_n_fib_below(limit: int, n: int) -> List[int]:
    """Return first n Fibonacci numbers strictly below 'limit'."""
    # Lazy pipeline: generate, cut off with takewhile, then slice n
    fibs = takewhile(lambda x: x < limit, fibonacci())
    first_n = islice(fibs, n)
    return list(first_n)


def group_words_by_initial(words: Iterable[str]) -> List[Tuple[str, List[str]]]:
    """Group consecutive words by their initial letter (case-insensitive)."""
    # For groupby to work as expected, data should be pre-sorted by the key.
    words = sorted(words, key=lambda w: w[:1].lower())
    grouped: List[Tuple[str, List[str]]] = []
    for key, group in groupby(words, key=lambda w: w[:1].lower()):
        grouped.append((key, list(group)))
    return grouped


def merge_three_streams(a: Iterable[T], b: Iterable[T], c: Iterable[T]) -> Iterator[T]:
    """Chain three streams lazily."""
    return chain(a, b, c)


# ------------------------------------------------------------
# 6) Realistic example: chunked file reader (iterator)
# ------------------------------------------------------------
# A classic iterator use-case is streaming large files in chunks so you don't
# load everything into memory.

class FileChunks(Iterator[bytes]):
    """Iterate over a file in fixed-size chunks."""

    def __init__(self, path: str, chunk_size: int = 8192) -> None:
        self._f = open(path, "rb")
        self._chunk_size = chunk_size

    def __iter__(self) -> "FileChunks":
        return self

    def __next__(self) -> bytes:
        chunk = self._f.read(self._chunk_size)
        if not chunk:
            self._f.close()
            raise StopIteration
        return chunk


# ------------------------------------------------------------
# 7) Best practices & pitfalls
# ------------------------------------------------------------
# If your object is a *collection*, make it an Iterable that returns a *new*
#  iterator each time (__iter__ should NOT return self in that case).
# Raise StopIteration to end iteration (generators do this automatically when they return).
# Prefer generators for simplicity and readability.
# Use itertools for fast, memory-efficient data pipelines.
# Provide __reversed__ when reverse iteration is a common/cheap operation.
#
#  Pitfall: Returning self from __iter__ on a *reusable* container may lead
#    to bugs if two loops iterate the same object at once (they'll share state).
#  Pitfall: Mutating a collection while iterating can cause surprises.
#  Pitfall: Infinite iterators (like fibonacci/count) must be bounded by
#    takewhile/islice or explicit breaks.

# ------------------------------------------------------------
# 8) Demonstration
# ------------------------------------------------------------
if __name__ == "__main__":
    print("1) Iterator protocol with Counter:")
    print(list(Counter(3, 7)))  # [3, 4, 5, 6]

    print("\n2) Iterable vs Iterator (MyRange creates fresh iterators):")
    r = MyRange(0, 5)
    # Two independent iterations:
    a = list(iter(r))
    b = list(iter(r))
    print("First pass :", a)  # [0, 1, 2, 3, 4]
    print("Second pass:", b)  # [0, 1, 2, 3, 4]

    print("\n3) Generators:")
    print("Evens up to 10:", list(evens_up_to(10)))
    print("Composed pipeline up to 8:", list(composed_pipeline(8)))
    # Infinite generators: take a few values safely
    print("First 7 Fibonacci:", list(islice(fibonacci(), 7)))  # [0, 1, 1, 2, 3, 5, 8]

    print("\n4) iter(callable, sentinel) and next(..., default):")
    print("Read until 0 sentinel:", iter_callable_demo())
    it = iter([10, 20])
    print("next with default (safe):", next(it, "END"), next(it, "END"), next(it, "END"))  # 10 20 END

    print("\n4b) reversed() via __reversed__:")
    logs = LogFileLines(["boot", "ready", "warn", "ok"])
    print("Forward :", list(logs))
    print("Backward:", list(reversed(logs)))

    print("\n5) itertools pipelines:")
    print("Top 5 fibs below 100:", top_n_fib_below(100, 5))
    words = ["Apple", "apricot", "banana", "Berry", "blue", "avocado"]
    print("Grouped words:", group_words_by_initial(words))
    merged = list(merge_three_streams([1, 2], (3, 4), range(5, 7)))
    print("Merged streams:", merged)

    print("\n6) FileChunks example (skipped in demo).")
    print("   Usage:")
    print('   for chunk in FileChunks("large.bin", 4096):')
    print("       process(chunk)")

    print("\n7) Summary:")
    print("- Use __iter__/__next__/StopIteration to implement iterators.")
    print("- Prefer generators for most iterator use-cases.")
    print("- Build lazy, memory-efficient pipelines with itertools.")
