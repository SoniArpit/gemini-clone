from pydantic import BaseModel
from typing import Optional

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None