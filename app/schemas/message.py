from pydantic import BaseModel

class MessageRequest(BaseModel):
    prompt: str