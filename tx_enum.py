from enum import Enum


class TxType(Enum):
    TRANSFER = 'transfer'
    SWAP = 'swap'
    BRIDGE = 'bridge'
