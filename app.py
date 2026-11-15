from flask import Flask, render_template, redirect, url_for, session, flash
from cart import Cart
from commands import AddItemCommand, RemoveItemCommand, ChangeQuantityCommand, CartInvoker
from catalog import FOOD_ITEMS

app = Flask(__name__)
app.secret_key = "replace-this-development-secret"

def get_cart():
    if "cart_items" not in session:
        session["cart_items"] = []
    return Cart.from_dict(session["cart_items"])

def save_cart(cart):
    session["cart_items"] = cart.to_dict()
    session.modified = True

@app.get("/")
def index():
    cart = get_cart()
    return render_template("index.html", foods=FOOD_ITEMS, cart=cart)

@app.post("/add/<int:item_id>")
def add(item_id):
    food = next((x for x in FOOD_ITEMS if x["id"] == item_id), None)
    if food is None:
        flash("Food item not found.", "error")
        return redirect(url_for("index"))
    cart = get_cart()
    invoker = CartInvoker()
    invoker.execute(AddItemCommand(cart, food))
    session["last_command"] = {"type": "add", "item": food}
    save_cart(cart)
    flash(f'{food["name"]} added to your cart.', "success")
    return redirect(url_for("index"))

@app.post("/remove/<int:item_id>")
def remove(item_id):
    cart = get_cart()
    item = next((x for x in cart.items if x["id"] == item_id), None)
    if item:
        invoker = CartInvoker()
        invoker.execute(RemoveItemCommand(cart, item_id))
        session["last_command"] = {"type": "remove", "item": item}
        save_cart(cart)
        flash(f'{item["name"]} removed.', "success")
    return redirect(url_for("index"))

@app.post("/quantity/<int:item_id>/<action>")
def quantity(item_id, action):
    if action not in ("increase", "decrease"):
        return redirect(url_for("index"))
    cart = get_cart()
    delta = 1 if action == "increase" else -1
    invoker = CartInvoker()
    invoker.execute(ChangeQuantityCommand(cart, item_id, delta))
    session["last_command"] = None
    save_cart(cart)
    return redirect(url_for("index"))

@app.post("/undo")
def undo():
    last = session.get("last_command")
    if not last:
        flash("There is no cart action to undo.", "error")
        return redirect(url_for("index"))
    cart = get_cart()
    if last["type"] == "add":
        cart.remove(last["item"]["id"])
    elif last["type"] == "remove":
        cart.add(last["item"])
    save_cart(cart)
    session["last_command"] = None
    flash("Last add/remove action undone.", "success")
    return redirect(url_for("index"))

@app.post("/clear")
def clear():
    session["cart_items"] = []
    session["last_command"] = None
    flash("Cart cleared.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
