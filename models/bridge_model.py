from Crypto.SelfTest.Protocol.test_ecdh import private_key
from sqlalchemy import Column, Integer, String

from models.base_model import BaseModel


class Bridge(BaseModel):
    __tablename__ = 'bridges'

    id = Column(Integer, private_key=True, autoincrement=True)
    src_chain = Column(String())
    dst_chain = Column(String())
