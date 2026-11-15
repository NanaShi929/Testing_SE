from customization import build_customized_food
from decorators import FoodItem, ExtraCheese, ExtraPatty, ExtraToppings, Jalapenos, SpecialSauce

BURGER = {"name": "Classic Burger", "price": 129}

def test_base_food_price_and_name():
    food = FoodItem("Burger", 100)
    assert food.get_name() == "Burger" if hasattr(food, "get_name") else food.get_description() == "Burger"
    assert food.get_cost() == 100

def test_single_decorator_adds_cost_and_description():
    food = ExtraCheese(FoodItem("Burger", 100))
    assert food.get_cost() == 125
    assert "Extra cheese" in food.get_description()

def test_multiple_decorators_stack():
    food = ExtraPatty(ExtraCheese(FoodItem("Burger", 100)))
    assert food.get_cost() == 165
    assert "Extra cheese" in food.get_description()
    assert "Extra patty" in food.get_description()

def test_builder_ignores_unknown_addons():
    food = build_customized_food(BURGER, ["cheese", "unknown"])
    assert food.get_cost() == 154

def test_builder_prevents_duplicate_addons():
    food = build_customized_food(BURGER, ["cheese", "cheese"])
    assert food.get_cost() == 154

def test_all_addons_calculation():
    food = build_customized_food(BURGER, ["cheese", "patty", "toppings", "jalapenos", "sauce"])
    assert food.get_cost() == 239

def test_no_addons_keeps_base_price():
    food = build_customized_food(BURGER, [])
    assert food.get_cost() == 129
