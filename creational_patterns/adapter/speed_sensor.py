""" Speed Sensor Adapter """

from abc import ABC, abstractmethod

class SpeedSensor(ABC):
    @abstractmethod
    def get_speed_kmh(self) -> float:
        pass

class USCar:
    def mph(self) -> float:
        return 60.0
    
class EUCar:
    def kph(self) -> float:
        return 100.0
    
class USCarAdapter(SpeedSensor):
    def __init__(self, car: USCar):
        self.car = car
    
    def get_speed_kmh(self) -> float:
        return self.car.mph() * 1.60934
    
class EUCarAdapter(SpeedSensor):
    def __init__(self, car: EUCar):
        self.car = car

    def get_speed_kmh(self) -> float:
        return self.car.kph()
    
sensor: SpeedSensor = USCarAdapter(USCar())
print(round(sensor.get_speed_kmh(), 1))
sensor = EUCarAdapter(EUCar())
print(sensor.get_speed_kmh())