from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.db import Base

class SubscriptionEvent(Base):
    __tablename__ = "subscription_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_type = Column(String, nullable=False)
    raw_event = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
