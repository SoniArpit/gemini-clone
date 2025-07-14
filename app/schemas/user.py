from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class TierEnum(str, Enum):
    basic = "basic"
    pro = "pro"

class UserResponse(BaseModel):
    id: UUID
    mobile: str
    tier: TierEnum

    class Config:
        orm_mode = True
