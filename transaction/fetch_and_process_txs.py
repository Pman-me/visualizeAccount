from transaction.analyze_tx_type import process_tx
from transaction.txs_data_per_chain import fetch_txs_per_chain


def fetch_and_process_txs(*, chains, api_base_url, api_key, account_address, tx_repo, logger):
    transactions = fetch_txs_per_chain(chains=chains, api_base_url=api_base_url, api_key=api_key,
                                       account_address=account_address, tx_repo=tx_repo, logger=logger)
    if not transactions:
        raise ValueError(f"The address {account_address} has no transactions.")
    process_tx(chains=chains, txs_per_chain=transactions, api_base_url=api_base_url,
               api_key=api_key, account_address=account_address, tx_repo=tx_repo, logger=logger)
