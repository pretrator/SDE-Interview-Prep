from abc import ABC, abstractmethod
from collections import deque

class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Kitchen:
    def prepare_dish(self, dish):
        print("Preparing: [",dish, ']' )
        # TODO: Print "Preparing: [dish]"
        pass

    def cancel_dish(self, dish):
        # TODO: Print "Cancelling: [dish]"
        print("Cancelling:[",dish,']' )
        pass

class PlaceOrderCommand(OrderCommand):
    def __init__(self, kitchen, dish):
        self.kitchen = kitchen
        self.dish = dish
        # TODO: Store receiver and dish
        pass

    def execute(self):
        self.kitchen.prepare_dish(self.dish)
        # TODO: Call kitchen.prepare_dish(dish)
        pass

    def undo(self):
        self.kitchen.cancel_dish(self.dish)
        # TODO: Call kitchen.cancel_dish(dish)
        pass

class CancelOrderCommand(OrderCommand):
    def __init__(self, kitchen, dish):
        self.kitchen = kitchen
        self.dish = dish
        # TODO: Store receiver and dish
        pass

    def execute(self):
        self.kitchen.cancel_dish(self.dish)
        # TODO: Call kitchen.cancel_dish(dish)
        pass

    def undo(self):
        self.kitchen.prepare_dish(self.dish)
        # TODO: Call kitchen.prepare_dish(dish)
        pass

class Waiter:
    def __init__(self):
        self.pendingq = deque([])
        self.history = []
        # TODO: Initialize pending queue and history stack
        pass

    def take_order(self, command):
        self.pendingq.append(command)
        # TODO: Add command to pending queue
        pass

    def submit_orders(self):
        while len(self.pendingq) > 0:
            command = self.pendingq.popleft()
            command.execute()
            self.history.append(command)
        # TODO: Execute all pending commands, move them to history
        pass

    def undo_last(self):
        command = self.history.pop()
        command.undo()
        # TODO: Pop the most recent command from history and call undo()
        pass

if __name__ == "__main__":
    kitchen = Kitchen()
    waiter = Waiter()
    waiter.take_order(PlaceOrderCommand(kitchen, "Pasta"))
    waiter.take_order(PlaceOrderCommand(kitchen, "Salad"))
    waiter.submit_orders()
    waiter.take_order(CancelOrderCommand(kitchen, "Salad"))
    waiter.submit_orders()
    waiter.undo_last()