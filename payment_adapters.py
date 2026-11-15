from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount, customer_name):
        raise NotImplementedError

    @staticmethod
    def make_receipt(success, method, customer, amount, reference):
        return {
            "success": success,
            "method": method,
            "customer": customer,
            "amount": round(amount, 2),
            "reference": reference,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }


class CardGateway:
    def make_card_payment(self, amount_in_rupees, cardholder):
        return {"status": "approved", "reference": "CARD-" + uuid4().hex[:8].upper(),
                "paid_amount": round(amount_in_rupees, 2), "payer": cardholder}


class UpiGateway:
    def send_upi_money(self, payment_details):
        return {"result": "SUCCESS", "transaction_id": "UPI-" + uuid4().hex[:8].upper(),
                "amount": round(payment_details["value"], 2), "customer": payment_details["name"]}


class WalletGateway:
    def debit_wallet(self, user, paise):
        return {"code": 200, "wallet_reference": "WALLET-" + uuid4().hex[:8].upper(),
                "debited_paise": int(paise), "account_name": user}


class CardPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or CardGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.make_card_payment(amount, customer_name)
        return self.make_receipt(response["status"] == "approved", "Card", response["payer"],
                             response["paid_amount"], response["reference"])


class UpiPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or UpiGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.send_upi_money({"value": amount, "name": customer_name})
        return self.make_receipt(response["result"] == "SUCCESS", "UPI", response["customer"],
                             response["amount"], response["transaction_id"])


class WalletPaymentAdapter(PaymentProcessor):
    def __init__(self, gateway=None):
        self.gateway = gateway or WalletGateway()

    def pay(self, amount, customer_name):
        response = self.gateway.debit_wallet(customer_name, round(amount * 100))
        return self.make_receipt(response["code"] == 200, "Wallet", response["account_name"],
                             round(response["debited_paise"] / 100, 2), response["wallet_reference"])


PAYMENT_METHODS = {
    "card": "Credit / Debit Card",
    "upi": "UPI",
    "wallet": "Digital Wallet",
}


def get_payment_processor(method):
    adapters = {"card": CardPaymentAdapter, "upi": UpiPaymentAdapter, "wallet": WalletPaymentAdapter}
    if method not in adapters:
        raise ValueError("Unsupported payment method.")
    return adapters[method]()
