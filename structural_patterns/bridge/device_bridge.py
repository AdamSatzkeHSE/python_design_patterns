""" Bridge Pattern 
Decoupling Remote controls (abstractions) from Devices (implementations) """


""" When you have two dimensions that vary independently, the Bridge let's you evolve them
separately.
- Abstraction: The high-level "thing" your app uses (e.g. Remote)
- Implementation: The low-level operations that can differ (e.g. a Device like a TV, Radio)
"""

""" Steps:
- Define Implementor interface (Device) -> Captures the minimal operations
- Keep the abstraction methods stable and high-level (Remote methods call Device)
- Compose them at runtime Remote(device)
"""
from abc import ABC, abstractmethod

class Device(ABC):
    @abstractmethod
    def power(self):
        pass

    @abstractmethod
    def volume(self, delta: int):
        pass

# Implementations
class TV(Device):
    def __init__(self):
        self.on = False
        self.vol = 10

    def power(self):
        self.on = not self.on
        print("TV power:", self.on)

    def volume(self, delta):
        self.vol = max(0, self.vol + delta)
        print("TV volume:", self.vol)

class Radio(Device):
    def __init__(self):
        self.on = False
        self.vol = 5

    def power(self):
        self.on = not self.on
        print("Radio power:", self.on)

    def volume(self, delta):
        self.vol = max(0, self.vol + delta)
        print("Radio volume:", self.vol)

# Abstractions
class Remote:
    def __init__(self, device: Device):
        self.device = device

    def toggle(self):
        self.device.power()

    def volume_up(self):
        self.device.volume(1)
    
    def volume_down(self):
        self.device.volume(-1)

if __name__ == "__main__":
    device = TV()
    r = Remote(device)
    r.toggle()
    r.vol_up()
    r.vol_down()

""" Why bridge and not adapter?
- Bridge splits one concept into two orthogonal hierarchies (remotes, devices) composed at runtime
- Adapter makes an incompatible API look like another: you'd use it to wrap a weird 3rd party device
too look like a Device.
- Strategy: swaps an algorithm behind one interface; it doesn't model two independent hierarchies.
"""

""" When to use it:
- When you foresee many combinations of two axes (UI vs. platform, model vs. storage, payment flow vs. gateway.)
- You need to compile or ship them independently (plugins, device drivers)
- You want to unit test each side separately
"""