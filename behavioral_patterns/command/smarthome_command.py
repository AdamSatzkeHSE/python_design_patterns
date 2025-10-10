""" The command pattern turns a request into a standalone object so you can:
- queue it
- log it
- undo/redo it
- compose it with other
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List

class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False

    def on(self):
        self.is_on = True
        print(f"[Light] {self.location}: ON")

    def off(self):
        self.is_on = False
        print(f"[Light] {self.location}: OFF")

class DoorLock:
    def __init__(self, door: str):
        self.door = door
        self.locked = False

    def lock(self):
        self.locked = True
        print(f"[Lock] {self.door}: LOCKED")

    def unlock(self):
        self.locked = False
        print(f"[Lock] {self.door}: UNLOCKED")


class Thermostat:
    def __init__(self):
        self.temp = 21

    def set_temp(self, value: int):
        old = self.temp
        self.temp = value
        print(f"[Thermostat] {old}grad C -> {self.temp}grad C")
        return old
    
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

# Concrete Commands
@dataclass
class LightOn(Command):
    light: Light
    
    def execute(self):
        self.light.on()
    
    def undo(self):
        self.light.off()

@dataclass
class LightOff(Command):
    light: Light
    
    def execute(self): 
        self.light.off()
    
    def undo(self): 
        self.light.on()

@dataclass
class LockDoor(Command):
    lock: DoorLock

    def execute(self): 
        self.lock.lock()

    def undo(self):    
        self.lock.unlock()

@dataclass
class UnlockDoor(Command):
    lock: DoorLock

    def execute(self):
        self.lock.unlock()

    def undo(self):
        self.lock.lock()

@dataclass
class SetTemperature(Command):
    tstat: Thermostat
    new_value: int
    _prev: Optional[int] = None

    def execute(self):
        self._prev = self.tstat.set_temp(self.new_value)

    def undo(self):
        if self._prev is not None:
            self.tstat.set_temp(self._prev)

@dataclass
class Macro(Command):
    commands: List[Command]
    # execute in order, undo in reverse order
    def execute(self):
        for c in self.commands:
            c.execute()
    def undo(self):
        for c in reversed(self.commands):
            c.undo()

# Invoker: The Remote
class Remote:
    def __init__(self):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def press(self, command: Command):
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            print("[Remote] Nothing to undo.")
            return
        cmd = self._undo_stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)

    def redo(self):
        if not self._redo_stack:
            print("[Remote] Nothing to redo.")
            return
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._undo_stack.append(cmd)

# Test

if __name__ == "__main__":
    living = Light("Living Room")
    front_door = DoorLock("Front Door")
    tstat = Thermostat()
    remote = Remote()

    # Single actions
    remote.press(LightOn(living))
    remote.press(SetTemperature(tstat, 23))
    remote.undo()
    remote.redo()

    # Macro: "Good Night"
    good_night = Macro([
        LightOff(living),
        LockDoor(front_door),

    ])

# Why this is useful

# Undo/redo: Built-in because each command knows how to reverse itself.

# Decoupling: The Remote (invoker) doesn’t know anything about lights, locks, or thermostats—it just runs commands.

# Composability: Macro lets you bundle routines like “Good Morning” or “Good Night.”

# Extensibility: Add a new device or action? Create a new command class; the remote stays unchanged.

# When to reach for it

# You need undo/redo, logging, audit trails, retry, scheduling, or queuing actions.

# You want a pluggable “button” or shortcut system where behavior can be swapped at runtime.