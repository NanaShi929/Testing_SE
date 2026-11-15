from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, session, flash
from catalog import FOOD_ITEMS
from cart import Cart
from commands import AddItemCommand, RemoveItemCommand, ChangeQuantityCommand, CartInvoker
from customization import build_customized_food, ADD_ONS
from discounts import get_discount_strategy, DISCOUNT_OPTIONS
from payment_adapters import get_payment_processor, PAYMENT_METHODS

app = Flask(__name__)
app.secret_key = "food-ordering-demo-secret"
invoker = CartInvoker()


def current_cart():
    return Cart.from_dict(session.get("cart", []))


def save_cart(cart):
    session["cart"] = cart.to_dict()
    session.modified = True


def bill_details(cart):
    subtotal = cart.total
    discount_name = session.get("discount_type", "none")
    discount = get_discount_strategy(discount_name).calculate_discount(subtotal)
    return subtotal, discount, round(max(0, subtotal - discount), 2)


@app.get("/")
def index():
    cart = current_cart()
    subtotal, discount, total = bill_details(cart)
    return render_template(
        "index.html", foods=FOOD_ITEMS, cart=cart.items, addons=ADD_ONS,
        discount_options=DISCOUNT_OPTIONS, discount_type=session.get("discount_type", "none"),
        subtotal=subtotal, discount=discount, total=total,
        payment_methods=PAYMENT_METHODS, receipt=session.get("receipt")
    )


@app.post("/cart/add/<int:food_id>")
def add_to_cart(food_id):
    food = next((item for item in FOOD_ITEMS if item["id"] == food_id), None)
    if not food:
        flash("That menu item could not be found.", "error")
        return redirect(url_for("index"))
    selected = request.form.getlist("addons")
    customized = build_customized_food(food, selected)
    cart = current_cart()
    line = {
        "id": uuid4().hex,
        "food_id": food_id,
        "name": customized.get_description(),
        "price": round(customized.get_cost(), 2),
        "quantity": 1,
        "base_name": food["name"],
    }
    invoker.execute(AddItemCommand(cart, line))
    save_cart(cart)
    flash(f'{line["name"]} added to your cart.', "success")
    return redirect(url_for("index"))


@app.post("/cart/quantity/<line_id>/<int:delta>")
def change_quantity(line_id, delta):
    if delta not in (-1, 1):
        return redirect(url_for("index"))
    cart = current_cart()
    invoker.execute(ChangeQuantityCommand(cart, line_id, delta))
    save_cart(cart)
    return redirect(url_for("index"))


@app.post("/cart/remove/<line_id>")
def remove_from_cart(line_id):
    cart = current_cart()
    invoker.execute(RemoveItemCommand(cart, line_id))
    save_cart(cart)
    flash("Item removed from your cart.", "success")
    return redirect(url_for("index"))


@app.post("/discount")
def apply_discount():
    choice = request.form.get("discount_type", "none")
    if choice not in DISCOUNT_OPTIONS:
        flash("Please choose a valid discount.", "error")
    else:
        session["discount_type"] = choice
        flash("Discount updated.", "success")
    return redirect(url_for("index"))


@app.post("/checkout")
def checkout():
    cart = current_cart()
    if not cart.items:
        flash("Add something to your cart before checkout.", "error")
        return redirect(url_for("index"))

    customer = request.form.get("customer_name", "").strip()
    method = request.form.get("payment_method", "")
    if not customer:
        flash("Enter your name to continue.", "error")
        return redirect(url_for("index"))
    if method not in PAYMENT_METHODS:
        flash("Choose a valid payment method.", "error")
        return redirect(url_for("index"))

    subtotal, discount, total = bill_details(cart)
    processor = get_payment_processor(method)
    receipt = processor.pay(total, customer)
    receipt.update({"subtotal": subtotal, "discount": discount, "items": cart.to_dict()})
    session["receipt"] = receipt
    session["cart"] = []
    session["discount_type"] = "none"
    session.modified = True
    flash("Your order has been placed.", "success")
    return redirect(url_for("index"))


@app.post("/receipt/clear")
def clear_receipt():
    session.pop("receipt", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
