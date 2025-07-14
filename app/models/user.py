from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum
from app.core.db import Base

class TierEnum(str, enum.Enum):
    basic = "basic"
    pro = "pro"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mobile = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    tier = Column(Enum(TierEnum), default=TierEnum.basic)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

