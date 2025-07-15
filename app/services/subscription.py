import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import redis
from app.core.config import settings
from app.models.user import User
from app.schemas.subscription import TierEnum

stripe.api_key = settings.STRIPE_SECRET_KEY
r = redis.Redis.from_url(settings.REDIS_URL)

def create_checkout_session(db: Session, user_id: str, price_id: str, success_url: str, cancel_url: str):
    """Create Stripe checkout session for Pro subscription"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create Stripe customer if not exists
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            metadata={"user_id": str(user_id)}
        )
        user.stripe_customer_id = customer.id
        db.commit()
    
    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'user_id': str(user_id)}
    )
    
    return {
        "checkout_url": session.url,
        "session_id": session.id
    }


def handle_webhook_event(db: Session, event_type: str, event_data: dict):
    """Handle Stripe webhook events"""
    if event_type == "checkout.session.completed":
        handle_checkout_completed(db, event_data)
    elif event_type == "customer.subscription.deleted":
        handle_subscription_deleted(db, event_data)


def handle_checkout_completed(db: Session, session_data):
    """Upgrade user to Pro after successful checkout"""
    user_id = session_data.get('metadata', {}).get('user_id')
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.tier = TierEnum.pro
            user.updated_at = datetime.now()
            db.commit()
            # Clear Redis usage cache
            r.delete(f"daily_usage:{user_id}")

def handle_subscription_deleted(db: Session, subscription_data):
    """Downgrade user to Basic after subscription cancellation"""
    customer_id = subscription_data.get('customer')
    if customer_id:
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.tier = TierEnum.basic
            user.updated_at = datetime.now()
            db.commit()

def get_daily_usage(user_id: str) -> int:
    """Get daily usage count from Redis"""
    key = f"daily_usage:{user_id}"
    usage = r.get(key)
    return int(usage) if usage else 0

def increment_daily_usage(user_id: str) -> int:
    """Increment daily usage counter with 24h expiry"""
    key = f"daily_usage:{user_id}"
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, 86400)  # 24 hours
    pipe.execute()
    return get_daily_usage(user_id)

def check_usage_limit(db: Session, user_id: str) -> bool:
    """Check if user can make more requests"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    if user.tier == TierEnum.pro:
        return True  
    
    # Basic users limited to 5 per day
    daily_usage = get_daily_usage(user_id)
    return daily_usage < 5

def get_subscription_status(db: Session, user_id: str):
    """Get user's subscription status"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    daily_limit = 5 if user.tier == TierEnum.basic else 999999  # Pro = unlimited
    daily_usage = get_daily_usage(user_id)
    
    return {
        "tier": user.tier,
        "daily_limit": daily_limit,
        "daily_usage": daily_usage,
        "remaining_usage": max(0, daily_limit - daily_usage)
    }


# Middleware for rate limiting
def rate_limit_middleware(db: Session, user_id: str):
    """Check and increment usage limits"""
    if not check_usage_limit(db, user_id):
        raise HTTPException(
            status_code=429, 
            detail="Daily limit exceeded. Upgrade to Pro for unlimited usage."
        )
    increment_daily_usage(user_id)
