from fastapi import APIRouter
from app.core.db import check_db_connection
import redis
from app.core.config import settings
import celery
from redis.exceptions import ConnectionError as RedisConnectionError
from celery.exceptions import OperationalError as CeleryOperationalError

router = APIRouter()

@router.get("/health")
def health_check():
    # Database status
    db_status = "connected" if check_db_connection() else "disconnected"
    
    # Redis status
    try:
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        redis_status = "connected" if redis_client.ping() else "disconnected"
    except RedisConnectionError:
        redis_status = "disconnected"
    
    # Celery status
    try:
        celery_status = "connected" if celery.current_app.control.ping() else "disconnected"
    except CeleryOperationalError:
        celery_status = "disconnected"
    
    return {
        "status": "ok",
        "database": db_status,
        "redis": redis_status,
        "celery": celery_status
    }