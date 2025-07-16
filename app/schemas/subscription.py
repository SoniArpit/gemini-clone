from pydantic import BaseModel
from app.models.user import TierEnum

class SubscriptionResponse(BaseModel):
    checkout_url: str
    session_id: str

class SubscriptionStatus(BaseModel):
    tier: TierEnum
    daily_limit: int
    daily_usage: int
    remaining_usage: int