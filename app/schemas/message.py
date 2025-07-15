from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.message import SenderEnum
from pydantic import ConfigDict


class MessageRequest(BaseModel):
    prompt: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chatroom_id: UUID
    sender: SenderEnum
    content: str
    created_at: datetime