from sqlalchemy import Column, String

from models.base_model import BaseModel


class AddressModel(BaseModel):
    __tablename__ = 'addresses'

    address = Column(String(42))
    owner = Column(String(42), nullable=True)
