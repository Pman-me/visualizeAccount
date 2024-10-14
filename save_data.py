import redis

from settings import Settings


def save_tx_data(settings: Settings, txs: list[dict]):
    rd = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASS,
                     db=settings.REDIS_DB_NO)
    with rd.pipeline(txs) as pipe:
        for id, tx in enumerate(txs, start=1):
            pipe.hsetnx('transactions', str(id), str(tx))

        pipe.execute()


def get_tx_data(settings: Settings):
    rd = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASS,
                     db=settings.REDIS_DB_NO, decode_responses=True)
    return rd.hgetall('transactions')
