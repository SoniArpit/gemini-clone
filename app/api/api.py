from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1 import auth
from app.api.v1 import user
from app.api.v1 import chatroom
from app.api.v1 import message
from app.api.v1 import subscription
from app.api.v1 import test

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(chatroom.router, prefix="/chatroom", tags=["Chatroom"])
api_router.include_router(message.router, prefix="/message", tags=["Message"])
api_router.include_router(subscription.router, prefix="/subscription", tags=["Subscription"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
