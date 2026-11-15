from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount follows the same calculation method."""

    @abstractmethod
    def calculate_discount(self, subtotal):
        raise NotImplementedError


class NoDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return 0.0


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def calculate_discount(self, subtotal):
        return round(max(0, subtotal) * self.percentage / 100, 2)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount):
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.amount = amount

    def calculate_discount(self, subtotal):
        return round(min(max(0, subtotal), self.amount), 2)


class get_discount_strategy:
    """Factory-like selector that returns the chosen Strategy object."""

    def __new__(cls, discount_type):
        strategies = {
            "none": NoDiscount(),
            "percentage": PercentageDiscount(10),
            "flat": FlatDiscount(50),
        }
        if discount_type not in strategies:
            raise ValueError("Unknown discount strategy.")
        return strategies[discount_type]


DISCOUNT_OPTIONS = {
    "none": "No discount",
    "percentage": "10% discount",
    "flat": "₹50 off",
}
