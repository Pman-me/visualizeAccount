from repository.tx_repo import TxRepo


def save_tx(swap_txs: [], tx_repo: TxRepo):
    for tx in swap_txs:
        tx_repo.set(tx, key=None)
