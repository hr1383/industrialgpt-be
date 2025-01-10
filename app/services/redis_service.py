import json
from typing import List
import redis
from app.models import Message, ChatResponseV2
from app.config import settings
import time
import json


class RedisService:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=settings.REDIS_URL, port=6379)
        # redis.from_url(settings.REDIS_URL, decode_responses=True)

    def chat_key(self, user_id, chat_id):
        return f"{user_id}:chat:{chat_id}:messages"

    def save_message(self, user_id: str, chat_id: str, message: Message, isNew: bool = False):
        # key = f"{user_id}:{message_id}"
        # self.redis_client.set(key, message.json())
        timestamp = time.time()  # Current timestamp in seconds
        # Key for storing messages
        redis_key = self.chat_key(user_id, chat_id)
        # Add the message to the sorted set with the timestamp as the score
        # print("storing" + message.json())
        if isNew:
            self.redis_client.rpush(user_id, chat_id)
        self.redis_client.zadd(redis_key, {message.json(): timestamp})

    def get_chat_history(self, user_id: str, message_id, start, limit: int = 5) -> List[Message]:
        # Get all keys for the user
        redis_key = self.chat_key(user_id, message_id)
        # Retrieve messages sorted by timestamp
        return self.redis_client.zrange(redis_key, start, start + limit)

    def get_chat_ids(self, user_id, start, limit: int = 100) -> List[Message]:
        # Get all keys for the user
        chat_ids = self.redis_client.lrange(user_id, 0, -1)
        print(chat_ids)
        result = []
        for chat_id in chat_ids:
            key = f"{user_id}:chat:{chat_id.decode('utf-8')}:messages"
            print(key)    
            oldest_messages = self.redis_client.zrange(key, 0, 0)
            if oldest_messages:
                message = Message.parse_raw(oldest_messages[0])
                result.append({
                    'id': chat_id,
                    'message': message.content[:50],
                    'timestamp': message.timestamp
                })
        return result

   

    # Example Usage
    # user_id = "user1"
    # chat_ids = get_chat_ids_for_user(user_id)
    # print(f"Chat IDs for {user_id}: {chat_ids}")
# m = Message(content = "hello",role = "user")
#
# RedisService().save_message("first", "1",{m.json:time.time()})
