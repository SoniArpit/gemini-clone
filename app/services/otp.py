import random
import redis
from typing import Optional
from app.core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))

def store_otp(mobile: str, otp: str) -> bool:
    """Store OTP in Redis with expiration"""
    try:
        key = f"otp:{mobile}"
        r.set(key, otp, ex=settings.OTP_EXPIRATION_MINUTES * 60)
        return True
    except redis.RedisError:
        return False

def verify_otp(mobile: str, otp: str) -> bool:
    """Verify OTP and delete if correct"""
    try:
        key = f"otp:{mobile}"
        stored_otp = r.get(key)
        
        if not stored_otp:
            return False
            
        if stored_otp == otp:
            r.delete(key)  # Delete OTP after successful verification
            return True
        return False
    except redis.RedisError:
        return False

def get_otp_ttl(mobile: str) -> Optional[int]:
    """Get remaining time for OTP in seconds"""
    try:
        key = f"otp:{mobile}"
        ttl = r.ttl(key)
        return ttl if ttl > 0 else None
    except redis.RedisError:
        return None