import json
from typing import List
import redis
from app.models import Message
from app.config import settings
import time
import json
class RedisService:
    def __init__(self):
        self.redis_client =redis.StrictRedis(host=settings.REDIS_URL, port=6379)
            # redis.from_url(settings.REDIS_URL, decode_responses=True)

    def chat_key(self,user_id, chat_id):
        return f"{user_id}:chat:{chat_id}:messages"

    def save_message(self, user_id: str, chat_id: str, message: Message):
        # key = f"{user_id}:{message_id}"
        # self.redis_client.set(key, message.json())
        timestamp = time.time()  # Current timestamp in seconds
        # Key for storing messages
        redis_key = self.chat_key(user_id,chat_id)
        # Add the message to the sorted set with the timestamp as the score
        print(redis_key)
        print("storing" + message.json())
        self.redis_client.zadd(redis_key, {message.json(): timestamp})

    def get_chat_history(self, user_id: str,message_id, start, limit: int = 5) -> List[Message]:
        # Get all keys for the user
        redis_key = self.chat_key(user_id, message_id)
        # Retrieve messages sorted by timestamp
        return self.redis_client.zrange(redis_key, start, start+limit)

    def get_chat_ids(self, user_id, start,limit:int = 5) -> List[Message]:
        # Get all keys for the user
        pattern = f"{user_id}:chat:*:messages"
        chat_ids = []
        cursor = 0

        # Use SCAN to find all keys matching the pattern
        while True:
            cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern)
            for key in keys:
                # Extract the chat_id from the key
                parts = key.decode('utf-8').split(':')
                print(parts)
                chat_ids.append(parts[2])  # Extract chat_id from the key
            if cursor == 0:
                break
        print(chat_ids)
        return chat_ids

    def get_chat_ids_for_user(self, user_id):
        pattern = f"{user_id}:chat:*:messages"
        chat_ids = []
        cursor = 0

        # Use SCAN to find all keys matching the pattern
        while True:
            cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern)
            for key in keys:
                # Extract the chat_id from the key
                parts = key.decode('utf-8').split(':')
                chat_ids.append(parts[3])  # Extract chat_id from the key
            if cursor == 0:
                break

        return chat_ids

    # Example Usage
    # user_id = "user1"
    # chat_ids = get_chat_ids_for_user(user_id)
    # print(f"Chat IDs for {user_id}: {chat_ids}")
# m = Message(content = "hello",role = "user")
#
# RedisService().save_message("first", "1",{m.json:time.time()})