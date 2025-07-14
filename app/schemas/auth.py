from pydantic import BaseModel, Field

class SignupRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number")

class SendOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number")

class VerifyOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number")
    otp: str = Field(min_length=4, max_length=6, description="OTP")

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"