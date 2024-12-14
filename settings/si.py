import os
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

# Database Settings
RDBMS_USER = ''
RDBMS_PASSWORD = ''
RDBMS_HOST = ''
RDBMS_PORT = 5432
RDBMS_DB = ''

# Redis Settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
MAIN_REDIS_DB = 0

# Addresses And Events Sig Hash
ZERO_ADDRESS = 0x0000000000000000000000000000000000000000
AccountAddress = ''
TRANSFER_EVENT_SIG_HASH = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
DEPOSIT_EVENT_SIG_HASH = 0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c
WITHDRAWAL_EVENT_SIG_HASH = 0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65

# Scale
NumberFloatingPoint = 18
SCALE = 10 ** NumberFloatingPoint
D_SCALE = Decimal(SCALE)

# Scan API Key
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ETHERSCAN_API_BASE_URL = 'https://api.etherscan.io/v2/api'
ETHERSCAN_API_URL_QUERY_PARAM = ''

# Chains Metadata
CHAINS = [
    {'chain_id': 8453, 'rpc': 'https://mainnet.base.org'},
    {'chain_id': 534352, 'rpc': 'https://rpc.scroll.io'},
]

# Dev Environment Settings
DEV_ENV = bool(os.getenv('DEV_ENV', default=False))


MAX_NONCE_PLATFORM_WALLET = 20000

NFT_INTERFACES_ID = [
    '0x80ac58cd',  # ERC721
    '0xd9b67a26',  # ERC1155
    '0x5b2312e3',  # ERC998
]