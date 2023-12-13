from pydantic import BaseModel
from database.models import Wallet


class WalletWithBalance(BaseModel):
    wallet: Wallet
    balance: int
