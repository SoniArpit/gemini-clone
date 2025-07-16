from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.chatroom import ChatroomCreateRequest, ChatroomResponse, ChatroomDetailResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User
import redis
from app.core.config import settings
from app.services.chatroom import create_chatroom_for_user, get_chatrooms_for_user, get_chatroom_by_id
router = APIRouter()

r = redis.Redis.from_url(settings.REDIS_URL)

@router.post("/", response_model=ChatroomResponse, status_code=status.HTTP_201_CREATED)
def create_chatroom(
    payload: ChatroomCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return create_chatroom_for_user(user.id, payload, db)

@router.get("/", response_model=list[ChatroomResponse])
def get_chatrooms(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_chatrooms_for_user(user.id, db)

@router.get("/{chatroom_id}", response_model=ChatroomDetailResponse)
def get_chatroom(
    chatroom_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_chatroom_by_id(chatroom_id, user.id, db)