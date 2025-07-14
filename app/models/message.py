from sqlalchemy import Column, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.core.db import Base

class SenderEnum(str, enum.Enum):
    user = "user"
    gemini = "gemini"

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chatroom_id = Column(UUID(as_uuid=True), ForeignKey("chatrooms.id"), nullable=False)
    sender = Column(Enum(SenderEnum), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    chatroom = relationship("Chatroom", backref="messages")
