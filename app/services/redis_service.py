from redis.asyncio import Redis
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = Redis.from_url(redis_url)
