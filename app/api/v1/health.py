from fastapi import APIRouter
from app.core.db import check_db_connection

router = APIRouter()

@router.get("/health")
def health_check():
    db_status = "connected" if check_db_connection() else "disconnected"
    return {
        "status": "ok",
        "database": db_status
    }
