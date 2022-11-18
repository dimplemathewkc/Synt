import redis
from app.core.config import settings
from app.integration.singleton import Singleton

redis_conf = {
    "host": settings.REDIS_HOST,
    "port": settings.REDIS_PORT,
    "db": settings.REDIS_DB,
    "charset": "utf-8",
    "decode_responses": True,
}


@Singleton
class RedisClient:
    def __init__(self):
        self._client = redis.Redis(**redis_conf)

    def get_client(self):
        if self.is_active():
            return self._client
        else:
            self.__init__()
            return self._client

    def is_active(self):
        return self._client.ping()
