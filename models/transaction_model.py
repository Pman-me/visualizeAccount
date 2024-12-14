from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float, Date

from models.base_model import BaseModel


class TransactionModel(BaseModel):

    __tablename__ = 'transactions'

    hash = Column(String(), primary_key=True)
    wallet = Column(String(42))
    to_contract_name = Column(String())
    send = Column(String())
    recv = Column(String())
    fee = Column(Float)
    nonce = Column(String())
    date_time = Column(String())
    chain_id = Column(String())
    type = Column(String())
    bridge_id = Column(Integer, nullable=True)
