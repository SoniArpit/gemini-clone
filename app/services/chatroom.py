from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.chatroom import Chatroom
from app.schemas.chatroom import ChatroomCreateRequest, ChatroomResponse
import redis
import json
from app.core.config import settings
from typing import List
from fastapi import HTTPException, status
from uuid import UUID
from sqlalchemy.exc import NoResultFound

r = redis.Redis.from_url(settings.REDIS_URL)

def create_chatroom_for_user(user_id, payload: ChatroomCreateRequest, db: Session) -> Chatroom:
    try:
        chatroom = Chatroom(
            id=uuid4(),
            user_id=user_id,
            title=payload.title,
            created_at=datetime.now()
        )
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)

        # Invalidate cache
        r.delete(f"user:{user_id}:chatrooms")
        return chatroom
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create chatroom"
        )

def get_chatrooms_for_user(user_id: str, db: Session) -> List[ChatroomResponse]:
    """Get chatrooms for a specific user with Redis caching"""
    try:
        key = f"user:{user_id}:chatrooms"
        cached = r.get(key)
        
        if cached:
            return json.loads(cached)

        chatrooms = (
            db.query(Chatroom)
            .filter(Chatroom.user_id == user_id)
            .order_by(Chatroom.created_at.desc())
            .all()
        )

        # Convert to Pydantic models and cache as dict
        response = [ChatroomResponse.model_validate(c) for c in chatrooms]
        cache_data = [chatroom.model_dump() for chatroom in response]
        
        r.setex(key, settings.CACHE_TTL_SECONDS, json.dumps(cache_data, default=str))
        
        return response
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chatrooms"
        )

   
def get_chatroom_by_id(chatroom_id: UUID, user_id: UUID, db: Session):
    try:
        chatroom = (
            db.query(Chatroom)
            .filter(Chatroom.id == chatroom_id)
            .filter(Chatroom.user_id == user_id)
            .one()
        )
        return ChatroomResponse.model_validate(chatroom)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatroom not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get chatroom"
        )