""" A facade is a thin, friendly API that sits in front of a complicated subsystems
It doesn't replace those systems, it just gives you a simple door to walk through.

- You still keep the underlying modules.
- You add one class (facade) that exposes high level methods
- Clients call the facade instead of using many low level objects.

"""

""" Example:
Smart Home with separate services: Lights, thermostat, blinds, music, and security.

1. Dim lights
2. Lower thermostat
3. Close blinds
4. Arm security
5. Stop music
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class LightSystem:
    def on(self, room: str, level: int=100) -> None:
        print(f"Lights {room}: ON at {level}%")
    
    def off(self, room: str) -> None:
        print(f"[Lights] {room}: OFF")

@dataclass
class Thermostat:
    current_temp : float = 21.0

    def set_target(self, celsius: float) -> None:
        print(f"[Thermostat] Target set to {celsius:.1f} grad C")
        self.current_temp = celsius

@dataclass
class BlindController:
    def lower(self, room: str) -> None:
        print(f"[Blinds] {room}: LOWERED")

    def raise_blinds(self, room: str) -> None:
        print(f"[Blinds] {room}: RAISED")

@dataclass
class MusicSystem:
    def play_playlist(self, name: str, room: Optional[str] = None) -> None:
        where = f" in {room}" if room else ""
        print(f"[Music] Playing '{name}'{where}")

    def stop(self) -> None:
        print("[Music] STOP")

@dataclass
class SecuritySystem:
    armed: bool = False

    def arm_stay(self) -> None:
        self.armed = True
        print("[Security] ARMED (stay)")

    def disarm(self) -> None:
        self.armed = False
        print("[Security] DISARMED")

# The Facade (simple API)
@dataclass 
class SmartHomeFacade:
    lights: LightSystem
    thermostat: Thermostat
    blinds: BlindController
    music: MusicSystem
    security: SecuritySystem

    # High-Level operations (routines)
    def good_morning(self) -> None:
        print("### GOOD MORNING ###")
        self.security.disarm()
        self.blinds.raise_blinds("Bedroom")
        self.lights.on("Bedroom", level=70)
        self.thermostat.set_target(21.5)
        self.music.play_playlist("Morning Rock", room="Kitchen")

    def good_night(self) -> None:
        print("### GOOD NIGHT ###")
        self.music.stop()
        self.lights.off("Living room")
        self.lights.on("Bedroom", level=20)
        self.blinds.lower("Bedroom")
        self.thermostat.set_target(18.5)
        self.security.arm_stay()

    def leave_home(self) -> None:
        print("### LEAVE HOME ROUTINE ###")
        for room in ("Kitchen", "Living room", "Bedroom", "Hallway"):
            self.lights.off(room)
        self.music.stop()
        self.blinds.lower("Living room")
        self.thermostat.set_target(17.0)
        self.security.arm_stay()

# Test
facade = SmartHomeFacade(
    lights=LightSystem(),
    thermostat=Thermostat(),
    blinds=BlindController(),
    music=MusicSystem(),
    security=SecuritySystem()
)

facade.good_morning()
facade.leave_home()
facade.good_night()
