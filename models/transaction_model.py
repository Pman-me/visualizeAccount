from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float

from models.base_model import BaseModel


class TransactionModel(BaseModel):

    __tablename__ = 'transactions'

    hash = Column(String(), primary_key=True)
    from_address = Column(String(42), ForeignKey('address.address', ondelete='cascade', onupdate='cascade'))
    to_contract_name = Column(String(42))
    send = Column(String())
    recv = Column(String())
    call_data = Column(String())
    fee = Column(Float)
    nonce = Column(Integer)
    timestamp = Column(DateTime(timezone=False))
    chain = Column(String())
    bridge_id = Column(Integer, ForeignKey('bridge.id', ondelete='cascade', onupdate='cascade'), nullable=True)
