import django

django.setup()

from payments.models import Payment
from flask import Flask, render_template, request, jsonify

from flask import Flask, redirect, request

import stripe

stripe.api_key = "sk_test_51NG1reElCYAj8tIuRhSIGeecZIpQTtmQxQEelOgnaD0L4uW5MWgXv8TS3IB9MvcqWISgehQirGTTqBLjgcBcM5NM00XsTc5eGh"

app = Flask(__name__, static_url_path="", static_folder="public")

YOUR_DOMAIN = "http://localhost:4242"


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": "{{PRICE_ID}}",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success.html",
            cancel_url=YOUR_DOMAIN + "/cancel.html",
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


if __name__ == "__main__":
    app.run(port=4242)


@app.route("/success", methods=["GET"])
def check_payment_success():
    session_id = request.args.get("session_id")

    # Retrieve the Stripe Checkout Session
    session = stripe.checkout.Session.retrieve(session_id)

    # Check the payment status
    if session.payment_status == "paid":
        return jsonify({"success": True, "message": "Payment successful"})
    else:
        return jsonify({"success": False, "message": "Payment not successful"})


if __name__ == "__main__":
    app.run(debug=True)
