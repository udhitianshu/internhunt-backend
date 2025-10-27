import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

def get_razorpay_client():
    """Initialize Razorpay client using environment variables."""
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    return razorpay.Client(auth=(key_id, key_secret))

def create_order(amount_in_rupees: int):
    """Creates a new Razorpay order."""
    client = get_razorpay_client()
    order = client.order.create({
        "amount": amount_in_rupees * 100,
        "currency": "INR",
        "payment_capture": 1
    })
    return order

def verify_payment(order_id: str, payment_id: str, signature: str):
    """Verifies Razorpay payment signature."""
    client = get_razorpay_client()
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return True
    except Exception:
        return False
