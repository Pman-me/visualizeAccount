from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float, Date

from models.base_model import BaseModel


class TransactionModel(BaseModel):

    __tablename__ = 'transactions'

    hash = Column(String(), primary_key=True)
    wallet = Column(String(42))
    to_contract_name = Column(String(42))
    send = Column(String())
    recv = Column(String())
    fee = Column(Float)
    nonce = Column(Integer)
    date_time = Column(String())
    chain = Column(String())
    type = Column(String())
    bridge_id = Column(Integer, nullable=True)
