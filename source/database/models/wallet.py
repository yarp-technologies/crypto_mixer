from database.db import Base
from cryptography_module import encode_data, decode_data
from sqlalchemy import Column, Integer, String, Boolean
from custom_types import *


class Wallet(Base):
    __tablename__ = "wallets"

    id: ID = Column(Integer, primary_key=True, index=True)
    is_active: Status = Column(Boolean, default=True, index=True)
    address: Address = Column(String)
    private_key: PrivateKey = Column(String)

    def __init__(self, **data):
        super().__init__(**data)
        self.private_key = encode_data(self.private_key)
    

    @property
    def decoded_private_key(self) -> str:
        return decode_data(self.private_key)
