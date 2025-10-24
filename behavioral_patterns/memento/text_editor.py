from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class EditorMemento:
    
    """An immutable Snapshot (memento) of the editor's state.
    Caretaker stores these but never inspects them
    """

    text: str
    cursor: int

class TextEditor:
    """Originator. Knows hot to create and restore its own mementos.
    """
    def __init__(self, s: str) -> None:
        self._text = ""
        self._cursor = 0

    # business logic
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def cursor(self) -> int:
        return self._cursor
    
    def type(self, s: str) -> None:
        # insert at cursor
        self._text = self._text[:self.cursor] + s + self._text[self._cursor:]
        self._cursor += len(s)

    def move_cursor(self, index: int) -> None:
        self._cursor = max(0, min(index, len(self._text)))

    def delete(self, n: int = 1) -> None:
        # delete n chars to the left of the cursor
        n = max(0, min(n, self._cursor))
        self._text = self._text[:self._cursor - n] + self._text[self._cursor]

    def _restore(self, m: EditorMemento) -> None:
        self._text = m.text
        self._cursor = m.cursor

class History:
    """Caretaker. Manages undo/redo stacks of mememtos.
    Does not care what's inside a memento.
    """
    def __init__(self, originator: TextEditor) -> None:
        self._originator = originator
        self._undo: List[EditorMemento] = []
        self._redo: List[EditorMemento] = []

    def snapshot(self) -> None:
        # Called before mutating action
        self._undo.append(self._originator._save())
        self._redo.clear() # new branch, redo history invalid

    def undo(self) -> bool:
        if not self._undo:
            return False
        
        current = self._originator._save()
        m = self._undo.pop()
        self._redo.append(current)
        self._originator._restore(m)

        return True
    
    def redo(self) -> bool:
        if not self._redo:
            return False
        current = self._originator._save()
        m = self._redo.pop()
        self._undo.append(current)
        self._originator._restore(m)

        return True
    
if __name__ == "__main__":
    editor = TextEditor()
    history = History(editor)

    # user types "Hello"
    history.snapshot()          # take snapshot BEFORE change
    editor.type("Hello")

    # space + "world"
    history.snapshot()
    editor.type(" world")

    # move cursor and insert "beautiful "
    history.snapshot()
    editor.move_cursor(6)       # after "Hello "
    editor.type("beautiful ")

    print(editor.text)  # "Hello beautiful world"

    # Undo twice
    history.undo()
    print(editor.text)  # "Hello world"

    history.undo()
    print(editor.text)  # "Hello"

    # Redo once
    history.redo()
    print(editor.text)  # "Hello world"

#     Why this is a good fit

# The editor is the originator. It knows how to pack/unpack its own state.

# _EditorMemento is immutable (frozen=True), so caretakers can’t tinker.

# History (caretaker) manages undo/redo stacks but never peeks at fields.