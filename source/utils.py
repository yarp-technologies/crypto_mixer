from database.models import Wallet
from blockchain_module import BlockchainConnector
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


class WalletWithBalance(BaseModel):
    wallet: Wallet
    balance: int


async def get_wallets_with_balances(blockchain_connector: BlockchainConnector, db_session: AsyncSession) -> list[WalletWithBalance]:
    wallets = await _get_wallets(db_session)
    return [WalletWithBalance(wallet=wallet, balance=await blockchain_connector.get_balance(wallet.address))
            for wallet in wallets]


async def _get_wallets(db_session: AsyncSession) -> list[Wallet]:
    query = select(Wallet).where(Wallet.is_active == True)
    wallets = await db_session.execute(query)
    return wallets.scalars().all()
