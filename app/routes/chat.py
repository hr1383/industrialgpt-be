from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from app.models import ChatRequest, ChatResponse, Message
from app.services.redis_service import RedisService
from app.services.openai_service import OpenAIService

router = APIRouter()
redis_service = RedisService()
openai_service = OpenAIService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get chat history
        history = redis_service.get_chat_history(request.user_id)
        
        # Get response from OpenAI
        response = await openai_service.get_chat_response(request.message, history)
        
        # Generate message ID using timestamp
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Save user message
        user_message = Message(
            content=request.message,
            role="user",
            timestamp=timestamp
        )
        redis_service.save_message(request.user_id, f"{message_id}_user", user_message)

        # Save assistant response
        assistant_message = Message(
            content=response,
            role="assistant",
            timestamp=timestamp
        )
        redis_service.save_message(request.user_id, f"{message_id}_assistant", assistant_message)

        return ChatResponse(
            response=response,
            message_id=message_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))