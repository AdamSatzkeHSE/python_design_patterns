from abc import ABC, abstractmethod

# Product
class Transport(ABC):
    @abstractmethod
    def deliver(self): pass

class Truck(Transport):
    def deliver(self):
        return "Delivering by land in a truck."

class Ship(Transport):
    def deliver(self):
        return "Delivering by sea in a ship."


# Creator (Factory Method)
class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport: 
        pass

class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()

class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


# Client
def client_code(factory: Logistics):
    transport = factory.create_transport()
    print(transport.deliver())

client_code(RoadLogistics())  # Truck
client_code(SeaLogistics())   # Ship
