import json
from typing import List
import redis
from app.models import Message
from app.config import settings

class RedisService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)

    def save_message(self, user_id: str, message_id: str, message: Message):
        key = f"{user_id}:{message_id}"
        self.redis_client.set(key, message.json())

    def get_chat_history(self, user_id: str, limit: int = 5) -> List[Message]:
        # Get all keys for the user
        pattern = f"{user_id}:*"
        keys = self.redis_client.keys(pattern)
        
        # Sort keys by message_id (timestamp) and get the last 'limit' messages
        messages = []
        for key in sorted(keys)[-limit:]:
            message_data = self.redis_client.get(key)
            if message_data:
                messages.append(Message.parse_raw(message_data))
        
        return messages