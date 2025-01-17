import dotenv
import os
import redis

class Config:
    def __init__(self):
        dotenv.load_dotenv()
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), decode_responses=True)
        self.backend_url = os.getenv("BACKEND_URL", "localhost:8000")
        self.backend_https = bool(os.getenv("BACKEND_HTTPS", "true") == "true")
