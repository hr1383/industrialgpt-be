from fastapi import (APIRouter, Body
, Request)
from datetime import datetime
import uuid, json, app.utils
from app.models import ChatRequest, ChatResponse, Message, Messages
from app.services.redis_service import RedisService
from app.services.openai_service import OpenAIService
from app.services.send_email import EmailService

router = APIRouter()
redis_service = RedisService()
openai_service = OpenAIService()
email_service = EmailService()

def save_chat(chat_id, user_message, user_id, is_new: bool):
    history = redis_service.get_chat_history(user_id, chat_id, 0)
    # Get response from OpenAI
    response = openai_service.get_chat_response(user_message, history)
    # print ("AI " + response)
    # Generate message ID using timestamp
    timestamp = datetime.utcnow().isoformat()
    # Save user message
    user_message_obj = Message(
        content=user_message,
        role="user",
        timestamp=timestamp
    )
    redis_service.save_message(user_id, f"{chat_id}", user_message_obj, is_new)
    # Save assistant response
    assistant_message = Message(
        content=response,
        role="assistant",
        timestamp=timestamp
    )
    redis_service.save_message(user_id, f"{chat_id}", assistant_message)
    return response


@router.post("/users/{user_id}/chat", response_model=ChatResponse)
def chat(user_id: str, request: ChatRequest):
    # try:
    chat_id = uuid.uuid4().__str__()
    response = save_chat(chat_id, request.message, user_id, True)
    return ChatResponse(
        response=response,
        chat_id=chat_id
    )


@router.post("/users/{user_id}/chat/{chat_id}", response_model=ChatResponse)
def chat(user_id: str, chat_id:str, request: ChatRequest):
    response = save_chat(chat_id, request.message, user_id, False)
    return ChatResponse(
        response=response,
        chat_id=chat_id
    )


@router.get("/users/{user_id}/chat/{chat_id}")
def chat(user_id: str, chat_id: str):
    history = redis_service.get_chat_history(user_id, chat_id, 0, 50)
    result = []
    for m in history:
        result.append(json.loads(m))
    return result


@router.get("/users/{user_id}/chats")
def chat(user_id: str):
    history = redis_service.get_chat_ids(user_id, 0)
    return history


import json


@router.post("/vapi/calls/end")
def calls(payload: dict = Body(...)):
    msg = app.utils.get_email_text(payload)
    print(msg)
    email_service.send_email(msg)
    return {"response": "true"}
