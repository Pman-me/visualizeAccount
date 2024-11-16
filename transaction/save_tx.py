from repository.tx_repo import TxRepo


def save_tx(tx, tx_repo: TxRepo):
    tx_repo.set(tx, key=None)
