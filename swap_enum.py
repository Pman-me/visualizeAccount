from enum import Enum


class TxType(Enum):
    TRANSFER = 0
    SWAP = 1
    BRIDGE = 2
