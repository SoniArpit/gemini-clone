from app.models.message import Message
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.core.db import SessionLocal
from fastapi import HTTPException, status
from app.models.message import SenderEnum
from app.tasks.gemini_tasks import generate_reply_task

def send_message(chatroom_id: str, message: str, user_id: str):
    if message.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    try:
        generate_reply_task.delay(str(chatroom_id), message, str(user_id))
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

def save_message_response(chatroom_id: str, prompt: str, reply: str, user_id: str):
    """
    Save user message and AI response to database
    """
    db = SessionLocal()
    try:
        # Save user message
        user_message = Message(
            chatroom_id=chatroom_id,
            sender=SenderEnum.user,  # Assuming you have USER enum value
            content=prompt,
        )
        db.add(user_message)
        db.flush()  # Get the ID without committing
        
        # Save AI response
        ai_message = Message(
            chatroom_id=chatroom_id,
            sender=SenderEnum.gemini,  # Assuming you have AI enum value
            content=reply,
        )
        db.add(ai_message)
        db.commit()
        
        # Return both messages
        return {
            'user_message': user_message,
            'ai_message': ai_message
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save message: {str(e)}"
        )
