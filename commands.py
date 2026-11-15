from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def undo(self):
        raise NotImplementedError


class AddItemCommand(Command):
    def __init__(self, cart, food):
        self.cart, self.food = cart, dict(food)

    def execute(self):
        self.cart.add(self.food)

    def undo(self):
        self.cart.remove(self.food["id"])


class RemoveItemCommand(Command):
    def __init__(self, cart, line_id):
        self.cart, self.line_id = cart, line_id
        self.removed_item = None

    def execute(self):
        self.removed_item = next((dict(x) for x in self.cart.items if x["id"] == self.line_id), None)
        self.cart.remove(self.line_id)

    def undo(self):
        if self.removed_item:
            self.cart.add(self.removed_item)


class ChangeQuantityCommand(Command):
    def __init__(self, cart, line_id, delta):
        self.cart, self.line_id, self.delta = cart, line_id, delta

    def execute(self):
        self.cart.change_quantity(self.line_id, self.delta)

    def undo(self):
        self.cart.change_quantity(self.line_id, -self.delta)


class CartInvoker:
    def execute(self, command):
        command.execute()
        return command
