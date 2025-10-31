""" The command pattern 

The command pattern turns a request into a first-class object
so you can:
- Parametrize and queue actions (UI Buttons, CLI, job queues)
- Log, undo/redo or replay actions later
- Decouple senders (invokers) from doers (receivers)"""

""" Key roles
- Command: an object with a uniform execute() method and often undo()
- Receiver: The thing that actually does the work
- Invoker: triggers commands (menu, button, scheduler)"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

# A lightweight Protocol
class Command(Protocol):
    def execute(self) -> None:
        pass

@dataclass
class Light:
    is_on: bool = False

    def turn_on(self) -> None:
        self.is_on = True
        print("Light ON")

    def turn_off(self) -> None:
        self.is_on = False
        print("Light OFF")

@dataclass
class TurnOn:
    light: Light

    def execute(self) -> None:
        self.light.turn_on()

@dataclass
class TurnOff:
    light: Light

    def execute(self) -> None:
        self.light.turn_off()

# Invoker: holds and triggers commands
class Remote:
    def __init__(self) -> None:
        self._slot: Command | None = None

    def set_slot(self, cmd: Command) -> None:
        self._slot = cmd

    def press(self) -> None:
        if self._slot:
            self._slot.execute()

# Test
if __name__ == "__main__":
    light = Light()
    remote = Remote()

    remote.set_slot(TurnOn(light))
    remote.press() # Light ON

    remote.set_slot(TurnOff(light))
    remote.press() # Light OFF

# The invoker only knows the Command interface, not how the light works
""" When to use

- You need undo/redo, history, logging
- You queue/defer work (GUI)
- You want to decouple UI from business logic
"""


