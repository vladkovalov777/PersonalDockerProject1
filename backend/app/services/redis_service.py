import redis
from settings import settings


class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
        )

    def set_key(self, key: str, value: str, ex: int):
        self.redis_client.set(key, value, ex=ex)

    def get(self, key):
        return self.redis_client.get(key)

    def delete(self, key: str):
        self.redis_client.delete(key)


redis_service = RedisService()