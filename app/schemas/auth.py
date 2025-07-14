from pydantic import BaseModel, Field

class SignupRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)

class SendOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)

class VerifyOtpRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)
    otp: str = Field(min_length=4, max_length=6)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=15)

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)