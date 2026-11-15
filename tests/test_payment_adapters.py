import pytest
from payment_adapters import (
    CardPaymentAdapter,
    UpiPaymentAdapter,
    WalletPaymentAdapter,
    get_payment_processor,
)


def test_card_adapter_returns_common_format():
    result = CardPaymentAdapter().pay(250, "Asha")
    assert result["success"] is True
    assert result["method"] == "Card"
    assert result["amount"] == 250
    assert result["customer"] == "Asha"
    assert result["reference"].startswith("CARD-")


def test_upi_adapter_returns_common_format():
    result = UpiPaymentAdapter().pay(125.50, "Ravi")
    assert result["success"] is True
    assert result["method"] == "UPI"
    assert result["amount"] == 125.50
    assert result["reference"].startswith("UPI-")


def test_wallet_adapter_converts_rupees_to_paise_and_back():
    result = WalletPaymentAdapter().pay(99.99, "Maya")
    assert result["success"] is True
    assert result["method"] == "Wallet"
    assert result["amount"] == 99.99
    assert result["reference"].startswith("WALLET-")


@pytest.mark.parametrize("method, expected", [
    ("card", "Card"),
    ("upi", "UPI"),
    ("wallet", "Wallet"),
])
def test_processor_selector(method, expected):
    result = get_payment_processor(method).pay(100, "Test User")
    assert result["method"] == expected


def test_unknown_payment_method_is_rejected():
    with pytest.raises(ValueError):
        get_payment_processor("crypto")
