from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddItemCommand(Command):
    def __init__(self, cart, food):
        self.cart, self.food = cart, food

    def execute(self):
        self.cart.add(self.food)

    def undo(self):
        self.cart.change_quantity(self.food["id"], -1)

class RemoveItemCommand(Command):
    def __init__(self, cart, item_id):
        self.cart, self.item_id = cart, item_id
        self.removed_item = None

    def execute(self):
        self.removed_item = next((x.copy() for x in self.cart.items if x["id"] == self.item_id), None)
        self.cart.remove(self.item_id)

    def undo(self):
        if self.removed_item:
            food = {k: v for k, v in self.removed_item.items() if k != "quantity"}
            for _ in range(self.removed_item["quantity"]):
                self.cart.add(food)

class ChangeQuantityCommand(Command):
    def __init__(self, cart, item_id, delta):
        self.cart, self.item_id, self.delta = cart, item_id, delta

    def execute(self):
        self.cart.change_quantity(self.item_id, self.delta)

    def undo(self):
        self.cart.change_quantity(self.item_id, -self.delta)

class CartInvoker:
    """Invoker: executes command objects."""
    def execute(self, command):
        command.execute()
        return command
