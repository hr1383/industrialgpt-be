from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid, json
from app.models import ChatRequest, ChatResponse, Message, Messages
from app.services.redis_service import RedisService
from app.services.openai_service import OpenAIService

router = APIRouter()
redis_service = RedisService()
openai_service = OpenAIService()


@router.post("/users/{user_id}/chat", response_model=ChatResponse)
def chat(user_id:str, request: ChatRequest):
    # try:
        # Get chat history
        chat_id = request.chat_id if request.chat_id else uuid.uuid4().__str__()
        #fix the start later
        history = redis_service.get_chat_history(user_id,chat_id,0)

        # Get response from OpenAI
        response = openai_service.get_chat_response(request.message, history)
        # print ("AI " + response)
        # Generate message ID using timestamp

        timestamp = datetime.utcnow().isoformat()

        # Save user message
        user_message = Message(
            content=request.message,
            role="user",
            timestamp=timestamp
        )
        redis_service.save_message(user_id, f"{chat_id}", user_message)

        # Save assistant response
        assistant_message = Message(
            content=response,
            role="assistant",
            timestamp=timestamp
        )
        redis_service.save_message(user_id, f"{chat_id}", assistant_message)

        return ChatResponse(
            response=response,
            chat_id=chat_id
        )
    # except Exception as e:
    #     print (e)
    #     raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/chat/{chat_id}")
def chat(user_id:str, chat_id: str):
    history = redis_service.get_chat_history(user_id, chat_id, 0,50)
    result = []
    for m in history:
        result.append(json.loads(m))
    return result

@router.get("/users/{user_id}/chats")
def chat(user_id:str):
    history = redis_service.get_chat_ids(user_id, 0)
    return history

