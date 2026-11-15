from decorators import FoodItem, ExtraCheese, ExtraPatty, ExtraToppings, Jalapenos, SpecialSauce

ADD_ONS = {
    "cheese": {"label": "Extra cheese", "price": 25},
    "patty": {"label": "Extra patty", "price": 40},
    "toppings": {"label": "Extra toppings", "price": 20},
    "jalapenos": {"label": "Jalapeños", "price": 15},
    "sauce": {"label": "Special sauce", "price": 10},
}

DECORATORS = {
    "cheese": ExtraCheese,
    "patty": ExtraPatty,
    "toppings": ExtraToppings,
    "jalapenos": Jalapenos,
    "sauce": SpecialSauce,
}


def build_customized_food(food_data, selected_addons):
    food = FoodItem(food_data["name"], food_data["price"])
    for addon in dict.fromkeys(selected_addons):
        decorator = DECORATORS.get(addon)
        if decorator:
            food = decorator(food)
    return food
