from decorators import (
    FoodItem, ExtraCheese, ExtraPatty, ExtraToppings, Jalapenos, SpecialSauce
)

# Prices are in INR. Each decorator wraps the previous FoodItem object.
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
    """Create a base food and wrap it with the selected decorators."""
    food = FoodItem(food_data["name"], food_data["price"])
    # Avoid applying the same add-on twice.
    for addon in dict.fromkeys(selected_addons):
        decorator = DECORATORS.get(addon)
        if decorator:
            food = decorator(food)
    return food

if __name__ == "__main__":
    sample = {"name": "Classic Burger", "price": 129}
    result = build_customized_food(sample, ["cheese", "patty"])
    print(result.get_description())
    print(f"Final price: ₹{result.get_cost():.2f}")
