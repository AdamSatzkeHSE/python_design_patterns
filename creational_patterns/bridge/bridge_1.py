""" Bridge Pattern 
Decoupling Remote controls (abstractions) from Devices (implementations) """

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