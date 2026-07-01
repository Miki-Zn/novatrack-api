import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db
from app.models.user import User, UserRole
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY

router = APIRouter()

class CheckoutResponse(BaseModel):
    checkout_url: str

@router.post("/create-checkout-session", response_model=CheckoutResponse)
def create_checkout_session(
    current_user: User = Depends(get_current_active_user)
):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "NovaTrack PRO Subscription",
                    "description": "Unlock unlimited projects and tasks"
                },
                "unit_amount": 999,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:3000/cancel",
        customer_email=current_user.email
    )
    
    return {"checkout_url": session.url}

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        
        if customer_email:
            user = db.query(User).filter(User.email == customer_email).first()
            if user:
                user.role = UserRole.ADMIN
                db.commit()

    return {"status": "success"}