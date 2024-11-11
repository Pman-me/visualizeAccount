import redis

from repository.base_repo import BaseRepo


class RedisRepo(BaseRepo):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port)

    def get(self, key: str):
        return self.client.get(key)

    def get_list(self, key: str):
        return self.client.lrange(key, 0, -1)

    def set(self, key: str, value):
        try:
            if isinstance(value, list):
                for item in value:
                    self.client.lpush(key, str(item))
        except Exception as err:
            pass

    def delete(self, key: str) -> None:
        self.client.delete(key)
