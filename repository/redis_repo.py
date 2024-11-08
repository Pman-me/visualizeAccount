import redis

from repository.base_repo import BaseRepo


class RedisRepo(BaseRepo):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port)

    def get(self, key: str):
        data = self.client.get(key)

    def set(self, key: str, value):
        self.client.set(key, value)

    def delete(self, key: str) -> None:
        self.client.delete(key)
