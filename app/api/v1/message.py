from fastapi import APIRouter, Depends, status
from app.utils.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.message import MessageRequest
from app.schemas.common import SuccessResponse
from app.models.user import User
from app.services.message import send_message
from app.tasks.gemini_tasks import generate_reply_task


router = APIRouter()

@router.post("/chatroom/{chatroom_id}/message", response_model=SuccessResponse, status_code=status.HTTP_202_ACCEPTED)
def send_message_endpoint(
    chatroom_id: UUID,
    payload: MessageRequest,
    user: User = Depends(get_current_user)
):
    send_message(str(chatroom_id), payload.message, str(user.id))
    # generate_reply_task.delay(str(chatroom_id), payload.message, str(user.id))
    
    return SuccessResponse(success=True, message="Message is being processed.")
