from pydantic import BaseModel, Field

class SignupRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)