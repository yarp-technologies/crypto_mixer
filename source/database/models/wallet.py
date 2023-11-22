from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean
from custom_types import *


class Wallet(Base):
    __tablename__ = "wallets"

    id: ID = Column(Integer, primary_key=True, index=True)
    is_active: Status = Column(Boolean, index=True)
    address: Address = Column(String)
    private_key: PrivateKey = Column(String)
