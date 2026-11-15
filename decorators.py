from abc import ABC, abstractmethod


class FoodComponent(ABC):
    @abstractmethod
    def get_description(self):
        raise NotImplementedError

    @abstractmethod
    def get_cost(self):
        raise NotImplementedError


class FoodItem(FoodComponent):
    def __init__(self, name, price):
        self.name = name
        self.price = float(price)

    def get_description(self):
        return self.name

    def get_cost(self):
        return self.price


class FoodDecorator(FoodComponent):
    def __init__(self, food):
        self.food = food

    def get_description(self):
        return self.food.get_description()

    def get_cost(self):
        return self.food.get_cost()


class ExtraCheese(FoodDecorator):
    def get_description(self):
        return f"{self.food.get_description()}, Extra cheese"

    def get_cost(self):
        return self.food.get_cost() + 25


class ExtraPatty(FoodDecorator):
    def get_description(self):
        return f"{self.food.get_description()}, Extra patty"

    def get_cost(self):
        return self.food.get_cost() + 40


class ExtraToppings(FoodDecorator):
    def get_description(self):
        return f"{self.food.get_description()}, Extra toppings"

    def get_cost(self):
        return self.food.get_cost() + 20


class Jalapenos(FoodDecorator):
    def get_description(self):
        return f"{self.food.get_description()}, Jalapeños"

    def get_cost(self):
        return self.food.get_cost() + 15


class SpecialSauce(FoodDecorator):
    def get_description(self):
        return f"{self.food.get_description()}, Special sauce"

    def get_cost(self):
        return self.food.get_cost() + 10
