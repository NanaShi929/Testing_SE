from flask import Flask, render_template, request, redirect, url_for, session, flash
from payment_adapters import get_payment_processor, PAYMENT_METHODS

app = Flask(__name__)
app.secret_key = "member-four-development-secret"


@app.get("/")
def index():
    return render_template(
        "index.html",
        methods=PAYMENT_METHODS,
        result=session.get("last_payment"),
    )


@app.post("/pay")
def pay():
    customer_name = request.form.get("customer_name", "").strip()
    amount_text = request.form.get("amount", "").strip()
    method = request.form.get("payment_method", "").strip()

    if not customer_name:
        flash("Please enter the customer name.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        flash("Please enter a valid payment amount.", "error")
        return redirect(url_for("index"))

    if amount <= 0:
        flash("Payment amount must be greater than zero.", "error")
        return redirect(url_for("index"))

    if method not in PAYMENT_METHODS:
        flash("Please select a valid payment method.", "error")
        return redirect(url_for("index"))

    processor = get_payment_processor(method)
    result = processor.pay(amount, customer_name)

    session["last_payment"] = result
    session.modified = True

    if result["success"]:
        flash("Payment simulated successfully.", "success")
    else:
        flash("Payment could not be processed.", "error")

    return redirect(url_for("index"))


@app.post("/clear")
def clear():
    session.pop("last_payment", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5004)
