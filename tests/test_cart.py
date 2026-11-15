from cart import Cart
from commands import AddItemCommand, RemoveItemCommand, ChangeQuantityCommand, CartInvoker

BURGER = {"id": 1, "name": "Burger", "price": 100, "emoji": "🍔"}

def test_add_item():
    cart = Cart()
    CartInvoker().execute(AddItemCommand(cart, BURGER))
    assert cart.count == 1
    assert cart.total == 100

def test_adding_same_item_increases_quantity():
    cart = Cart()
    cart.add(BURGER)
    cart.add(BURGER)
    assert cart.items[0]["quantity"] == 2
    assert cart.total == 200

def test_remove_item():
    cart = Cart()
    cart.add(BURGER)
    CartInvoker().execute(RemoveItemCommand(cart, 1))
    assert cart.count == 0

def test_remove_command_undo():
    cart = Cart()
    cart.add(BURGER)
    command = RemoveItemCommand(cart, 1)
    command.execute()
    command.undo()
    assert cart.count == 1

def test_change_quantity_and_undo():
    cart = Cart()
    cart.add(BURGER)
    command = ChangeQuantityCommand(cart, 1, 1)
    command.execute()
    assert cart.count == 2
    command.undo()
    assert cart.count == 1

def test_decrease_to_zero_removes_item():
    cart = Cart()
    cart.add(BURGER)
    cart.change_quantity(1, -1)
    assert cart.count == 0

def test_cart_serialization():
    cart = Cart()
    cart.add(BURGER)
    restored = Cart.from_dict(cart.to_dict())
    assert restored.total == 100
    assert restored.items == cart.items
