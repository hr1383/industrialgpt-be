from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    content: str
    role: str
    timestamp: str

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    message_id: str