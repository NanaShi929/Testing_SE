from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class PaymentProcessor(ABC):
    """Target interface: the application uses this common payment method."""

    @abstractmethod
    def pay(self, amount, customer_name):
        raise NotImplementedError


# These gateway classes intentionally expose different method names and
# argument formats, as third-party payment services often do.
class CardGateway:
    def make_card_payment(self, amount_in_rupees, cardholder):
        return {
            "status": "approved",
            "reference": "CARD-" + uuid4().hex[:8].upper(),
            "paid_amount": round(amount_in_rupees, 2),
            "payer": cardholder,
        }


class UpiGateway:
    def send_upi_money(self, payment_details):
        return {
            "result": "SUCCESS",
            "transaction_id": "UPI-" + uuid4().hex[:8].upper(),
            "amount": round(payment_details["value"], 2),
            "customer": payment_details["name"],
        }


class WalletGateway:
    def debit_wallet(self, user, paise):
        return {
            "code": 200,
            "wallet_reference": "WALLET-" + uuid4().hex[:8].upper(),
            "debited_paise": int(paise),
            "account_name": user,
        }


class CardPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or CardGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.make_card_payment(amount, customer_name)
        return {
            "success": response["status"] == "approved",
            "method": "Card",
            "customer": response["payer"],
            "amount": response["paid_amount"],
            "reference": response["reference"],
            "message": "Card payment approved (simulation).",
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }


class UpiPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or UpiGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.send_upi_money({
            "value": amount,
            "name": customer_name,
        })
        return {
            "success": response["result"] == "SUCCESS",
            "method": "UPI",
            "customer": response["customer"],
            "amount": response["amount"],
            "reference": response["transaction_id"],
            "message": "UPI payment successful (simulation).",
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }


class WalletPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or WalletGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.debit_wallet(customer_name, round(amount * 100))
        return {
            "success": response["code"] == 200,
            "method": "Wallet",
            "customer": response["account_name"],
            "amount": round(response["debited_paise"] / 100, 2),
            "reference": response["wallet_reference"],
            "message": "Wallet payment successful (simulation).",
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }


PAYMENT_METHODS = {
    "card": "Credit / Debit Card",
    "upi": "UPI",
    "wallet": "Digital Wallet",
}


def get_payment_processor(method):
    adapters = {
        "card": CardPaymentAdapter,
        "upi": UpiPaymentAdapter,
        "wallet": WalletPaymentAdapter,
    }
    if method not in adapters:
        raise ValueError("Unsupported payment method.")
    return adapters[method]()
