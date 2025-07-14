from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(user_id: str) -> str:
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode = {"user_id": str(user_id), "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
