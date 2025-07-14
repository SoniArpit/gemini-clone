from fastapi import APIRouter
from app.api.v1 import health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, tags=["Health"])
