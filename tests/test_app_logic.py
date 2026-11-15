from cart import Cart
from commands import AddItemCommand, ChangeQuantityCommand, RemoveItemCommand, CartInvoker
from customization import build_customized_food
from discounts import get_discount_strategy
from payment_adapters import get_payment_processor


def test_cart_commands_add_change_and_remove():
    cart = Cart()
    invoker = CartInvoker()
    food = {"id": "line-1", "name": "Burger", "price": 100, "quantity": 1}
    invoker.execute(AddItemCommand(cart, food))
    invoker.execute(ChangeQuantityCommand(cart, "line-1", 1))
    assert cart.count == 2
    invoker.execute(RemoveItemCommand(cart, "line-1"))
    assert cart.count == 0


def test_decorator_adds_selected_extras_to_food():
    food = build_customized_food({"name": "Burger", "price": 100}, ["cheese", "patty"])
    assert food.get_description() == "Burger, Extra cheese, Extra patty"
    assert food.get_cost() == 165


def test_discount_strategies_calculate_correctly():
    assert get_discount_strategy("percentage").calculate_discount(200) == 20
    assert get_discount_strategy("flat").calculate_discount(200) == 50
    assert get_discount_strategy("flat").calculate_discount(30) == 30


def test_payment_adapters_return_common_receipt_format():
    for method in ("card", "upi", "wallet"):
        receipt = get_payment_processor(method).pay(100, "Test Customer")
        assert receipt["success"] is True
        assert receipt["amount"] == 100
        assert receipt["customer"] == "Test Customer"
        assert receipt["reference"]
