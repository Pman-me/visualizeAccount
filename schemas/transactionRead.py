from pydantic import BaseModel


class TransactionRead(BaseModel):
    hash: str
    wallet: str
    send: str | None
    recv: str | None
    date_time: str
    chain: str
    type: str

    class Config:
        from_attributes = True
