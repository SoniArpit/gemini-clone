from app.models.message import Message
from app.core.db import SessionLocal
from fastapi import HTTPException, status
from app.models.message import SenderEnum
from app.tasks.gemini_tasks import generate_reply_task
from app.models.chatroom import Chatroom
from sqlalchemy.orm import Session

def send_message(chatroom_id: str, prompt: str, db: Session):
    if not prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt cannot be empty"
        )

    # Check if chatroom exists
    chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()
    if not chatroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatroom not found"
        )

    try:
        generate_reply_task.delay(str(chatroom_id), prompt)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

def save_message_response(chatroom_id: str, prompt: str, reply: str):
    """
    Save user prompt and AI response to database
    """
    db = SessionLocal()
    try:
        # Save user message
        user_message = Message(
            chatroom_id=chatroom_id,
            sender=SenderEnum.user,
            content=prompt,
        )
        db.add(user_message)
        db.flush() 
        
        # Save AI response
        ai_message = Message(
            chatroom_id=chatroom_id,
            sender=SenderEnum.gemini,
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
