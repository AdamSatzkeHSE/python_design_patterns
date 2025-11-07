from abc import ABC, abstractmethod

# ===== Receivers =====
class Light:
    def __init__(self, name="Living Room"):
        self.name = name
        self.is_on = False

    def on(self):
        self.is_on = True
        print(f"{self.name} light: ON")

    def off(self):
        self.is_on = False
        print(f"{self.name} light: OFF")


class Fan:
    def __init__(self, name="Ceiling Fan"):
        self.name = name
        self.speed = 0  # 0=off, 1=low, 2=medium, 3=high

    def set_speed(self, speed: int):
        self.speed = speed
        label = ["off", "low", "medium", "high"][speed]
        print(f"{self.name}: speed -> {label} ({speed})")


# ===== Command Interface =====
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...


# ===== Concrete Commands =====
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.off()

    def undo(self):
        self.light.on()


class FanSetSpeedCommand(Command):
    def __init__(self, fan: Fan, target_speed: int):
        self.fan = fan
        self.target_speed = target_speed
        self.prev_speed = None

    def execute(self):
        self.prev_speed = self.fan.speed
        self.fan.set_speed(self.target_speed)

    def undo(self):
        if self.prev_speed is not None:
            self.fan.set_speed(self.prev_speed)


# ===== Invoker =====
class Remote:
    def __init__(self):
        self.history = []

    def press(self, cmd: Command):
        cmd.execute()
        self.history.append(cmd)

    def undo(self):
        if not self.history:
            print("Nothing to undo.")
            return
        cmd = self.history.pop()
        cmd.undo()


# ===== Demo / Test =====
if __name__ == "__main__":
    light = Light("Hall")
    fan = Fan("Bedroom Fan")
    remote = Remote()

    # Light on/off
    remote.press(LightOnCommand(light))
    remote.press(LightOffCommand(light))

    # Fan high then low
    remote.press(FanSetSpeedCommand(fan, 3))
    remote.press(FanSetSpeedCommand(fan, 1))

    # Undo twice
    print("-- undo --")
    remote.undo()  # fan back to 3
    remote.undo()  # fan back to previous before 3 (likely 0/off)

    # Extra undo attempts
    print("-- extra undo --")
    remote.undo()  # undo LightOff -> LightOn
    remote.undo()  # undo LightOn -> LightOff
    remote.undo()  # nothing left
