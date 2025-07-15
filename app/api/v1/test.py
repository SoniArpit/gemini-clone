from fastapi import APIRouter

router = APIRouter()

@router.get("/success")
async def payment_success(session_id: str = None):
    """Test endpoint for successful payment"""
    return {
        "message": "🎉 Payment successful! Your account has been upgraded to Pro.",
        "session_id": session_id,
        "status": "success",
        "note": "Check your account status at /api/v1/subscription/status"
    }

@router.get("/cancel")
async def payment_cancel():
    """Test endpoint for cancelled payment"""
    return {
        "message": "❌ Payment cancelled. You're still on the Basic plan.",
        "status": "cancelled"
    }