from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest
from app.schemas.common import SuccessResponse
from app.utils.dependencies import get_db
from app.services.auth import get_user_by_mobile, create_user

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
        message="Signup successful. Please verify OTP."
    )
    