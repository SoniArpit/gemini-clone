from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID
from datetime import datetime
from app.schemas.message import MessageResponse

class ChatroomCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Chatroom title")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        # Remove leading/trailing whitespace
        v = v.strip()
        if not v:
            raise ValueError('Title cannot be empty or just whitespace')
        return v

class ChatroomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    user_id: UUID
    created_at: datetime

class ChatroomDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    user_id: UUID
    created_at: datetime
    messages: list[MessageResponse]
