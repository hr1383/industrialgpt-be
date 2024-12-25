from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    content: str
    role: str
    timestamp: str

class Messages(BaseModel):
    messages: List[Message]


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    chat_id: str

class ChatResponseV2(BaseModel):
    response: dict
    chat_id: str
