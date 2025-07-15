from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db, get_current_user
from app.services.subscription import (
    create_checkout_session,
    handle_webhook_event,
    get_subscription_status
)
from app.schemas.subscription import SubscriptionResponse, SubscriptionStatus
from app.models.user import User
import stripe
from app.core.config import settings


router = APIRouter()

@router.post("/subscribe/pro", response_model=SubscriptionResponse)
async def subscribe_pro(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate Pro subscription via Stripe Checkout"""
    try:
        result = create_checkout_session(
            db=db,
            user_id=str(current_user.id),
            price_id=settings.STRIPE_PRO_PRICE_ID,
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL
        )
        return SubscriptionResponse(**result)
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events (no auth required)"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    handle_webhook_event(db, event['type'], event['data']['object'])
    return {"status": "success"}

@router.get("/subscription/status", response_model=SubscriptionStatus)
async def subscription_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's current subscription status"""
    return get_subscription_status(db, str(current_user.id))

