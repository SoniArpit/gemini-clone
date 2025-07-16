from fastapi import APIRouter, Depends, status
from app.utils.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.message import MessageRequest
from app.schemas.common import SuccessResponse
from app.models.user import User
from app.services.message import send_message
from app.services.subscription import rate_limit_middleware


router = APIRouter()

@router.post("/chatroom/{chatroom_id}/message", response_model=SuccessResponse, status_code=status.HTTP_202_ACCEPTED)
def send_message_endpoint(
    chatroom_id: UUID,
    payload: MessageRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rate_limit_middleware(db=db, user_id=str(user.id))
    send_message(str(chatroom_id), payload.prompt, db)
    
    return SuccessResponse(success=True, message="Message is being processed.")
