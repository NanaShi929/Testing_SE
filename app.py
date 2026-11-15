from flask import Flask, render_template, request, redirect, url_for, session, flash
from catalog import FOOD_ITEMS
from discounts import get_discount_strategy, DISCOUNT_OPTIONS

app = Flask(__name__)
app.secret_key = "member-three-development-secret"


@app.get("/")
def index():
    cart = session.get("cart", [])
    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    discount_type = session.get("discount_type", "none")
    strategy = get_discount_strategy(discount_type)
    discount_amount = strategy.calculate_discount(subtotal)
    total = max(0, subtotal - discount_amount)

    return render_template(
        "index.html",
        foods=FOOD_ITEMS,
        cart=cart,
        subtotal=subtotal,
        discount_amount=discount_amount,
        total=total,
        discount_type=discount_type,
        discount_options=DISCOUNT_OPTIONS,
    )


@app.post("/add/<int:food_id>")
def add_to_cart(food_id):
    food = next((item for item in FOOD_ITEMS if item["id"] == food_id), None)
    if food is None:
        flash("Food item not found.", "error")
        return redirect(url_for("index"))

    cart = session.get("cart", [])
    existing = next((item for item in cart if item["id"] == food_id), None)
    if existing:
        existing["quantity"] += 1
    else:
        cart.append({
            "id": food["id"],
            "name": food["name"],
            "price": float(food["price"]),
            "quantity": 1,
        })

    session["cart"] = cart
    session.modified = True
    flash(f'{food["name"]} added to cart.', "success")
    return redirect(url_for("index"))


@app.post("/remove/<int:food_id>")
def remove_from_cart(food_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != food_id]
    session["cart"] = cart
    session.modified = True
    flash("Item removed from cart.", "success")
    return redirect(url_for("index"))


@app.post("/discount")
def apply_discount():
    discount_type = request.form.get("discount_type", "none")
    if discount_type not in DISCOUNT_OPTIONS:
        flash("Please select a valid discount.", "error")
        return redirect(url_for("index"))

    session["discount_type"] = discount_type
    session.modified = True
    flash("Discount option updated.", "success")
    return redirect(url_for("index"))


@app.post("/clear")
def clear_cart():
    session["cart"] = []
    session["discount_type"] = "none"
    session.modified = True
    flash("Cart cleared.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5003)
