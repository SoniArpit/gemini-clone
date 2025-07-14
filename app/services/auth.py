from sqlalchemy.orm import Session
from app.models.user import User
import uuid
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def get_user_by_mobile(db: Session, mobile: str):
    return db.query(User).filter(User.mobile == mobile).first()

def create_user(db: Session, mobile: str) -> User:
    """Create a new user with comprehensive error handling"""
    try:
        # Double-check before creating (race condition protection)
        existing_user = get_user_by_mobile(db, mobile)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this mobile number already exists"
            )
        
        new_user = User(
            id=uuid.uuid4(),
            mobile=mobile,
            is_verified=False,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this mobile number already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )