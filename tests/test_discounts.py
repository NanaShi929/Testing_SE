import pytest
from discounts import NoDiscount, PercentageDiscount, FlatDiscount, get_discount_strategy


def test_no_discount():
    assert NoDiscount().calculate_discount(200) == 0


def test_percentage_discount():
    assert PercentageDiscount(10).calculate_discount(200) == 20


def test_flat_discount():
    assert FlatDiscount(50).calculate_discount(200) == 50


def test_flat_discount_cannot_exceed_subtotal():
    assert FlatDiscount(50).calculate_discount(30) == 30


def test_percentage_must_be_valid():
    with pytest.raises(ValueError):
        PercentageDiscount(120)


def test_factory_selects_percentage_strategy():
    strategy = get_discount_strategy("percentage")
    assert strategy.calculate_discount(100) == 10


def test_unknown_strategy_is_rejected():
    with pytest.raises(ValueError):
        get_discount_strategy("unknown")
