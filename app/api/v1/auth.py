from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, SendOtpRequest, VerifyOtpRequest, AuthResponse, ForgotPasswordRequest, ChangePasswordRequest
from app.schemas.common import SuccessResponse
from app.utils.dependencies import get_db, get_current_user
from app.services.auth import get_user_by_mobile, create_user
from app.services.otp import generate_otp, store_otp, verify_otp, get_otp_ttl
from app.services.jwt import create_access_token
from app.services.hash import hash_password, verify_password
from app.models.user import User

router = APIRouter()

@router.post("/signup", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = get_user_by_mobile(db, payload.mobile)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    create_user(db, payload.mobile)

    return SuccessResponse(
        success=True,
        message="Signup successful. Please send OTP to verify."
    )
    
@router.post("/send-otp", response_model=SuccessResponse)
def send_otp(payload: SendOtpRequest, db: Session = Depends(get_db)):
    user = get_user_by_mobile(db, payload.mobile)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    otp = generate_otp()
    
    if not store_otp(payload.mobile, otp):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate OTP. Please try again."
        )

    return SuccessResponse(
        success=True, 
        message="OTP sent successfully. Please verify OTP.",
        data={
            "otp": otp
        }
    )

@router.post("/verify-otp", response_model=AuthResponse)
def verify_otp_endpoint(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    user = get_user_by_mobile(db, payload.mobile)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # if user.is_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User is already verified"
    #     )

    if not verify_otp(payload.mobile, payload.otp):
        # Check if OTP exists or expired
        ttl = get_otp_ttl(payload.mobile)
        if ttl:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired or not found"
            )

    # Update user verification status
    try:
        user.is_verified = True
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify user"
        )

    # Generate access token
    token = create_access_token(user.id)

    return AuthResponse(
        access_token=token,
        message="OTP verified successfully"
    )


@router.post("/forgot-password", response_model=SuccessResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_mobile(db, payload.mobile)
    if not user:
        raise HTTPException(404, "User not found")

    otp = generate_otp()
    store_otp(payload.mobile, otp)

    return SuccessResponse(success=True, message="OTP sent for password reset. Please verify OTP", data={"otp": otp})


@router.post("/change-password", response_model=SuccessResponse)
def change_password(
    payload: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Just set hashed password unconditionally
    user.hashed_password = hash_password(payload.new_password)
    db.commit()

    return SuccessResponse(success=True, message="Password changed successfully.")