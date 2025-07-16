from pydantic import BaseModel, Field

class SignupRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number", example="1234567890", pattern=r"^\d+$")

class SendOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number", example="1234567890", pattern=r"^\d+$")

class VerifyOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number", example="1234567890", pattern=r"^\d+$")
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$", description="6-digit OTP code", example="123456")

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15, description="Mobile number", example="1234567890", pattern=r"^\d+$")

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6, description="New password")