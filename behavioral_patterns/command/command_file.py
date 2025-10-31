""" The Command design pattern helps us encapsulate an operation (undo, redo, copy, paste) as an object.
That this means is that we create a class taht contains all the logic and the mthods required to implement the operation
"""

""" Advantages:
- We don't have to execute a command directly. It can be executed at will.
- The object that invokes the command is decoupled from the object that knows how to perform it.
- The invoker does not need to know any implementation details about the command
- If it makes sense, multiple commands can be grouped to allow the invoker to execute them in order."""

""" command_file.py
- Create a file and optionally writing text (a string) to it
- Reading the contents of a file
- Renaming a file
- Deleting a file
"""

import os
verbose = True

# Command: Initialization and Executions
class RenameFile:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def execute(self):
        if verbose:
            print(f"[renaming {self.src} to {self.dest}]")

    def undo(self):
        if verbose:
            print(f"[renaming {self.dest} back to {self.src}")
        os.rename(self.dest, self.src)

def delete_file(path):
    if verbose:
        print(f"deleting file {path}")
    os.remove(path)

class CreateFile:
    def __init__(self, path, txt="Hello World\n"):
        self.path = path
        self.txt = txt

    def execute(self):
        if verbose:
            print(f"[creating file {self.path}]")
        with open(self.path, mode='w', encoding='utf-8') as out_file:
            out_file.write(self.txt)    
        
    def undo(self):
        delete_file(self.path)

class ReadFile:
    def __init__(self, path):
        self.path = path

    def execute(self):
        if verbose:
            print(f"[reading file {self.path}]")
        with open(self.path, mode="r", encoding="utf-8") as in_file:
            print(in_file.read(), end="")

if __name__ == "__main__":
    orig_name, new_name = "file1", "file2"
    commands = (
        CreateFile(orig_name),
        ReadFile(orig_name),
        RenameFile(orig_name, new_name)
    )
    [c.execute() for c in commands]
    answer = input("Reverse the executed commands? [y/n]")
    if answer not in "yY":
        print(f"The result is {new_name}")
        exit()

    for c in reversed(commands):
        try:
            c.undo()
        except AttributeError as e:
            print("Error", str(e))


