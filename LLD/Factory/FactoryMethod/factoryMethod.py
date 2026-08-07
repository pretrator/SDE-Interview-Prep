from abc import ABC, abstractmethod

# 1. Product Interface
class Transport(ABC):
    @abstractmethod
    def deliver(self):
        pass

# 2. Concrete Products
class Truck(Transport):
    def deliver(self):
        return "Delivering by land in a box"

class Ship(Transport):
    def deliver(self):
        return "Delivering by sea in a container"

# 3. The Creator Abstract Class
class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        # The Factory Method
        pass

    def plan_delivery(self):
        # The core business logic relies on the product returned by the factory method
        transport = self.create_transport()
        return f"Planning: {transport.deliver()}"

# 4. Concrete Creators
class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()

class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()

# Client Code
logistics = RoadLogistics()
print(logistics.plan_delivery())  # Output: Planning: Delivering by land in a box