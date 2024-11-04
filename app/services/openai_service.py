import openai
from typing import List
from app.models import Message
from app.config import settings

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def get_chat_response(self, prompt: str, history: List[Message] = None) -> str:
        messages = []
        
        # Add chat history if available
        if history:
            for msg in history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content