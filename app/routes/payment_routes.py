# app/routes/payment_routes.py
from fastapi import APIRouter, Body, HTTPException
from app.utils.payment_helper import create_order, verify_payment

router = APIRouter(prefix="/api/payment", tags=["Payments"])

@router.post("/create-order")
def create_order_route(payload: dict = Body(...)):
    amount = payload.get("amount")
    if not amount:
        raise HTTPException(status_code=400, detail="amount (in INR) is required")
    try:
        order = create_order(int(amount))
        return {"success": True, "order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify")
def verify_route(payload: dict = Body(...)):
    order_id = payload.get("order_id")
    payment_id = payload.get("payment_id")
    signature = payload.get("signature")
    if not all([order_id, payment_id, signature]):
        raise HTTPException(status_code=400, detail="order_id, payment_id and signature are required")
    ok = verify_payment(order_id, payment_id, signature)
    if ok:
        return {"success": True, "message": "Payment verified"}
    raise HTTPException(status_code=400, detail="Verification failed")
