from custom_types import Status, TxHash, Address
from blockchain_module import Transaction, BlockchainConnector
from database.models import Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Iterable
import random


class InputTxModule:
    def __init__(self,
                 blockchain_connector: BlockchainConnector,
                 db_session: AsyncSession):
        self.blockchain_connector = blockchain_connector
        self.db_session = db_session

    async def generate_transaction(self, address_from: Address, amount: int) -> Transaction:
        if amount < 1:
            raise ValueError("Amount must be greater than 0")
        if not await self._check_balance(amount):
            raise ValueError("Not enough balance")
        wallet = await self._get_random_wallet()
        tx = Transaction(
            address_from=address_from,
            address_to=wallet.address,
            value=amount,
        )
        await self.blockchain_connector.fill_tx(tx)
        return tx

    async def _check_balance(self, amount: int) -> Status:
        active_wallets = await self._get_active_wallets()
        total_balance = sum(await self.blockchain_connector.get_balance(
            wallet.address) for wallet in active_wallets)
        return total_balance >= amount

    async def _get_active_wallets(self) -> Iterable[Wallet]:
        query = select(Wallet).where(Wallet.is_active == True)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def _get_random_wallet(self) -> Wallet:
        query = select(Wallet).where(Wallet.is_active == True)
        wallets = await self.db_session.execute(query)
        wallets_list = wallets.scalars().all()
        return random.choice(wallets_list)

    async def check_transaction(self, tx_hash: TxHash, value: int) -> Status:
        tx = await self.blockchain_connector.get_tx(tx_hash)
        if tx is None:
            return False
        return tx.value >= value
