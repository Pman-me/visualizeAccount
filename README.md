# Transaction Processing System

## Overview

The Transaction Processing System is designed to interact with multiple blockchain networks, fetching and processing transactions for a specified account address. It categorizes transactions into different types (transfer, swap, bridge) and saves the relevant transaction data to a database. The system leverages the Web3 library to connect to Ethereum-compatible blockchains and utilizes a modular approach for transaction processing.


### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Install the required packages:
   ```bash
    pip install pydantic_settings==2.5.2 redis==5.1.0 requests==2.32.3 web3==6.20.3 SQLAlchemy~=2.0.36 pycryptodome~=3.20.0

### Usage

To execute the transaction processing system, run the following command:
   ```bash
   python main.py
   ```

### Transaction Fetching

- **fetch_txs_per_chain**: This function retrieves transactions for a specified account address from multiple blockchain networks. It filters out transactions that have errors and applies additional filtering based on the maximum nonce to ensure only relevant transactions are processed.

### Transaction Filtering

- **filter_txs_by_max_nonce**: This function filters transactions based on the maximum nonce per chain. It ensures that only transactions with a nonce greater than the maximum nonce are returned, preventing the processing of outdated transactions.

### Transaction Processing

- **process_tx**: This function processes the transactions retrieved for each blockchain network and categorizes them based on their type (transfer, swap, bridge).

### Token Transfer Logs Processing

- **process_token_transfer_logs**: This function processes the logs of token transfers and maps the details to the corresponding token addresses, identifying the amount transferred and the parties involved.

### Transaction Categorization

- **categorize_tx**: This function categorizes transactions into different types based on the transaction logs and details. It checks for transfer, swap, and bridge transactions and prepares them for saving.
- 
### Data Transformation

- **transform_tx_data**: This function transforms the transaction data into a structured format suitable for saving into the database, including details like transaction hash, wallet address, fees, and transaction type.

### Transaction Type Processing
- **process_transfer_tx**: This function processes transfer transactions and determines the amounts sent and received.
- **process_swap_tx**: This function processes swap transactions and determines the amounts sent and received for each token involved.
- **process_bridge_tx**: This function processes bridge transactions and determines the amounts sent and received, including native coins.

### Proxy Contract Detection

- **check_unstructured_proxy**: This function checks if a given contract address is an unstructured proxy by examining the storage at a specific slot (the implementation slot).

- **is_eip1967_proxy**: This function checks if a given contract address is an EIP-1967 compliant proxy by checking specific storage slots for the implementation and beacon addresses.

### Contract Interaction

- **get_contract_abi**: This function retrieves the ABI (Application Binary Interface) of a smart contract using an API call.

- **get_contract_name**: This function retrieves the name of a smart contract using an API call.

- **get_token_symbol**: This function retrieves the symbol of a token from its contract.

- **get_token_decimal**: This function retrieves the decimal precision of a token from its contract.

### Utility Functions

- **check_contract_address**: This function checks if a given address is a proxy contract and returns the appropriate contract address.

- **get_token_details**: This function retrieves the amount and currency of a token based on the transaction logs and contract details.