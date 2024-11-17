from typing import Optional

import redis

from repository.base_repo import BaseRepo


class RedisRepo(BaseRepo):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port)

    def get(self, key: str):
        return self.client.get(key)

    def get_hash(self, hash_name: str):
        return self.client.hgetall(hash_name)

    def set_hash(self, hash_name: str, values):
        try:
            for field, value in values:
                self.client.hset(hash_name, field, value)
        except Exception as err:
            pass

    def set(self, data: dict, /, key: Optional[str],):
        pass

    def delete(self, key: str) -> None:
        self.client.delete(key)
