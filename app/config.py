import dotenv
import os
import redis

class Config:
    def __init__(self):
        dotenv.load_dotenv()
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), decode_responses=True)
