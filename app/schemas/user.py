from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum
from uuid import UUID

class TierEnum(str, Enum):
    basic = "basic"
    pro = "pro"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(min_length=36, max_length=36, description="UUID string")
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number")
    tier: TierEnum = Field(description="User subscription tier")
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v