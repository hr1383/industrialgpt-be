from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    content: str
    role: str
    timestamp: str

class Messages(BaseModel):
    messages: List[Message]


class ChatRequest(BaseModel):
    # user_id: str
    chat_id: Optional[str]
    message: str

class ChatResponse(BaseModel):
    response: str
    chat_id: str