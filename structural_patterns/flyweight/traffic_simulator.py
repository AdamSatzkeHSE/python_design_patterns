""" Flyweight pattern
Share immutable, heavy, intrinsic data across many
lightweight objects. Pass any varying, extrinsic data at use time.

When to use:
You have a huge numbers of similar objects
(map markers, text glyphs, game titles) and memory is getting crushed

Benefits:
Big memory savings and faster creation times
Caveats:
Intrinsic state must be immutable: factories/caches may need thread safety if used concurrently
"""

""" traffic_simulator.py
Simulation of tens of thousands of cars in a city
Most cars are the same few models and don't change. (candidates for flyweight objects)

Each car instance needs dynamic fields like id, x, y, speed, heading (extrinsic state)"""

from dataclasses import dataclass
from typing import Dict, Tuple
from weakref import WeakValueDictionary

@dataclass(frozen=True)
class CarModel:
    make: str
    model: str
    year: int
    # PRetend these are big blobs (mesh, texture, specs)
    mesh_bytes: bytes
    texture_bytes: bytes
    engine_spec: str

    def render(self, x: float, y: float, heading_deg: float, plate: str) -> None:
        """Use the shared model data plus extrinsic state (positino, heading, etc.)
        to draw or update the car in the world.

        Args:
            x (float): _description_
            y (float): _description_
            heading_def (float): _description_
            plate (str): _description_
        """
        print(f"Render {self.make} {self.model} ({self.year}) at ({x:.1f}, {y:.1f})")
        print(f"heading {heading_deg:.0f} plate {plate}")


# Flyweight factory: returns "shared" CarModel instances
class CarModelFactory:
    def __init__(self) -> None:
        # WeakValueDictionary lets models be garbage collected if no one holds them.
        self._pool: "WeakValueDictionary[Tuple[str, str, int], CarModel]" = WeakValueDictionary()
    
    def get(self, make: str, model: str, year: int) -> CarModel:
        key = (make, model, year)
        car_model = self._pool.get(key)
        if car_model is None:
            # simulate heavy loading work
            print(f"[Factory] Loading heavy stuff for {key} once...")
            car_model = CarModel(
                make=make,
                model=model,
                year=year,
                mesh_bytes=b"/x200" * 2_000_000,
                texture_bytes=b"/x00" * 2_000_000,
                engine_spec="2.0L V3"
            )
            self._pool[key] = car_model
        return car_model

    def stats(self) -> int:
        return len(self._pool)
    
# Context objects: tiny, many, reference the shared model
@dataclass
class Car:
    plate: str
    x: float
    y: float
    heading_deg: float
    model: CarModel # The flyweight reference

    def tick(self, dt: float) -> None:
        # Update extrinsic state
        self.x += dt * 5
        self.heading_deg = (self.heading_deg  + dt * 3) % 360

    def draw(self) -> None:
        # Pass exstrinsic state to the shared flyweight
        self.model.render(self.x, self.y, self.heading_deg, self.plate)

if __name__ == "__main__":
    factory = CarModelFactory()

    # Create a lot of cars but only a couple of shared models
    civic_model = factory.get("Honda", "Civic", 2022)
    model3 = factory.get("Tesla", "Model3", 2023)

    cars = []
    for i in range(50000):
        if i % 3:
            model = civic_model
        else:
            model = model3
        cars.append(
            Car(
                plate=f"XYZ-{i:05d}",
                x=i % 500,
                y=(i // 500) % 500,
                heading_deg=(i * 7) % 360,
                model=model
            )
        )
    print(f"Unique CarModel flyweights: {factory.stats()}")  # -> 2
    print(f"Total cars (contexts): {len(cars)}")             # -> 50000

    # Use the cars (render a few frames of a few cars)
    for c in cars[:3]:
        c.draw()
        c.tick(0.16)
        c.draw()
