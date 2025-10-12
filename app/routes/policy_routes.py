from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(os.path.dirname(BASE_DIR), "pages")

@router.get("/privacy-policy", response_class=HTMLResponse)
def privacy_policy():
    with open(os.path.join(PAGES_DIR, "privacy_policy.html"), "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@router.get("/terms", response_class=HTMLResponse)
def terms():
    with open(os.path.join(PAGES_DIR, "terms.html"), "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@router.get("/refund-policy", response_class=HTMLResponse)
def refund_policy():
    with open(os.path.join(PAGES_DIR, "refund_policy.html"), "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@router.get("/shipping-policy", response_class=HTMLResponse)
def shipping_policy():
    with open(os.path.join(PAGES_DIR, "shipping_policy.html"), "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")
