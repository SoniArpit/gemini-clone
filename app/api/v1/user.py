from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user