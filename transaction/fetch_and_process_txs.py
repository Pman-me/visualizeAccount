from transaction.analyze_tx_type import process_tx
from transaction.txs_data_per_chain import fetch_txs_per_chain


def fetch_and_process_txs(chain_data, account_address, tx_repo):
    transactions = fetch_txs_per_chain(chain_data, account_address, tx_repo)
    if not transactions:
        raise ValueError(f"The address {account_address} has no transactions.")
    process_tx(chain_data, transactions, account_address, tx_repo)
