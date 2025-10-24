""" The mediator design pattern
It centralizes communication between objects (called colleagues) in a mediator so they
don't talk to each other directly
Result: fewer tight couplings and simpler colleague classes.

Calssic real-life analogy: an air traffic control tower (mediator) coordinating aircraft (colleagues)
Planes don't negotiate with each other. The tower orchestrates who lands/takes off and when.
"""

""" When to use:
Many objects would otherwise form a web of references (N2 interactions)
Coordination rules belong to a single place that can evolve
GUIs, chat rooms, multiplayer game lobbies, smart-home hubs

Benefits:
- Lower coupling between objects
- Easier to change orchestration rules

Trade off:
- Mediator can become complex. split by domain or layer policies."""

from dataclasses import dataclass, field
from typing import List, Optional, Protocol
import heapq

# Mediator interface
class ControlTower(Protocol):
    def register(self, aircraft: "Aircraft") -> None:
        pass
    def request_landing(self, aircraft: "Aircraft") -> None:
        pass
    def landing_complete(self, aircraft: "Aircraft") -> None:
        pass
    def declare_emergency(self, aircraft: "Aircraft") -> None:
        pass
    def broadcast(self, sender, msg: str) -> None:
        pass

# Colleague
@dataclass
class Aircraft:
    callsign: str
    fuel_minutes: int
    tower: ControlTower

    def __post_init__(self):
        self.tower.register(self)

    # Aircrew actions (these never contact other planes directly)
    def request_landing(self):
        self.tower.request_landing(self)

    def landing_complete(self):
        self.tower.landing_complete(self)
    
    def declare_emergency(self, reason: str):
        self.tower.declare_emergency(self, reason)

    # Tower - plane
    def notify(self, msg: str):
        print(f"[{self.callsign}] {msg}")

# Concrete mediator
@dataclass
class SimpleControlTower:
    runway_busy: bool = True

    _queue: List[tuple[int, int, Aircraft]] = field(default_factory=list)
    _counter: int = 0
    _aircraft: List[Aircraft] = field(default_factory=list)

    def register(self, aircraft: Aircraft) -> None:
        self._aircraft.append(aircraft)
        aircraft.notify("Registered with tower.")

    def _enqueue(self, aircraft: Aircraft, priority: int) -> None:
        self._counter += 1
        heapq.heappush(self._queue, (priority, self._counter, aircraft))

    def request_landing(self, aircraft: Aircraft) -> None:
        # Priority predominantly by fuel (less fuel → higher priority)
        priority = aircraft.fuel_minutes
        self._enqueue(aircraft, priority)
        self.broadcast(aircraft, f"{aircraft.callsign} requested landing (fuel {aircraft.fuel_minutes} min).")
        self._try_dispatch()

    def declare_emergency(self, aircraft: Aircraft, reason: str) -> None:
        # Emergencies jump the queue with strongest priority
        self._enqueue(aircraft, priority=-10)
        self.broadcast(aircraft, f"EMERGENCY from {aircraft.callsign}: {reason}")
        self._try_dispatch()

    def landing_complete(self, aircraft: Aircraft) -> None:
        if not self.runway_busy:
            aircraft.notify("Landing completion received, but runway was idle. (No-op)")
            return
        self.runway_busy = False
        self.broadcast(aircraft, f"{aircraft.callsign} cleared runway.")
        self._try_dispatch()

    def _try_dispatch(self) -> None:
        if self.runway_busy:
            return
        # Pop until we find someone not already on runway (simple model assumes unique)
        if not self._queue:
            return
        _, _, next_ac = heapq.heappop(self._queue)
        self.runway_busy = True
        next_ac.notify("Cleared to land NOW. Runway 27 free.")
        self.broadcast(next_ac, f"{next_ac.callsign} cleared to land.")

    def broadcast(self, sender: Aircraft, msg: str) -> None:
        # Tower can inform others; colleagues don't talk to each other directly
        for ac in self._aircraft:
            if ac is not sender:
                ac.notify(f"TOWER: {msg}")
        # Optionally let sender know too
        sender.notify(f"TOWER (ack): {msg}")

    # ===== Demo =====
if __name__ == "__main__":
    tower = SimpleControlTower()

    a1 = Aircraft("DAL123", fuel_minutes=45, tower=tower)
    a2 = Aircraft("UAE77",  fuel_minutes=25, tower=tower)
    a3 = Aircraft("EZY902", fuel_minutes=15, tower=tower)

    a1.request_landing()         # joins queue
    a2.request_landing()         # lower fuel → higher priority
    a3.request_landing()         # lowest fuel → lands first

    # After first aircraft lands and clears, the tower assigns next one automatically
    a3.landing_complete()

    # An emergency preempts the queue
    a1.declare_emergency("Smoke in cabin")
    a2.landing_complete()        # clears runway for the emergency
    a1.landing_complete()