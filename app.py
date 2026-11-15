from flask import Flask, render_template, request, redirect, url_for, session, flash
from customization import build_customized_food, ADD_ONS
from catalog import FOOD_ITEMS

app = Flask(__name__)
app.secret_key = "member-two-development-secret"

@app.get("/")
def index():
    return render_template(
        "index.html",
        foods=FOOD_ITEMS,
        orders=session.get("customized_items", []),
        addons=ADD_ONS,
        total=sum(item["price"] for item in session.get("customized_items", []))
    )

@app.post("/customize/<int:food_id>")
def customize(food_id):
    food = next((item for item in FOOD_ITEMS if item["id"] == food_id), None)
    if food is None:
        flash("Food item not found.", "error")
        return redirect(url_for("index"))

    selected_addons = request.form.getlist("addons")
    customized = build_customized_food(food, selected_addons)

    orders = session.get("customized_items", [])

# Store customized food details in dictionary format
    orders.append({
        "name": customized.get_description(),
        "price": customized.get_cost()
        })
    session["customized_items"] = orders
    session.modified = True

    flash(
        f'{customized.get_description()} added to your customization list.',"success"
        )
    return redirect(url_for("index"))

@app.post("/remove/<int:index>")
def remove(index):
    orders = session.get("customized_items", [])
    if 0 <= index < len(orders):
        removed = orders.pop(index)
        session["customized_items"] = orders
        session.modified = True
        flash(f'{removed["name"]} removed.', "success")
    return redirect(url_for("index"))

@app.post("/clear")
def clear():
    session["customized_items"] = []
    session.modified = True
    flash("Your customization list was cleared.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5002)
