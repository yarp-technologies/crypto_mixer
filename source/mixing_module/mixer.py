from .schemas import WalletWithBalance
from custom_types import Address
from blockchain_module import Transaction, Credentials, BlockchainConnector
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_wallets_with_balances
import random


class Mixer:
    def __init__(self,
                 blockchain_connector: BlockchainConnector,
                 db_session: AsyncSession):
        self.blockchain_connector = blockchain_connector
        self.db_session = db_session

    async def execute_tx(self, address_to: Address, amount: int):
        if amount < 1:
            raise ValueError("Amount must be greater than 0")
        wallets_with_balances = await get_wallets_with_balances(self.blockchain_connector, self.db_session)
        while amount > 0:
            iteration_amount = random.randint(1, amount)
            await self._fill_iteration(wallets_with_balances, iteration_amount, address_to)
            amount -= iteration_amount

    async def _fill_iteration(self, wallets_with_balances: list[WalletWithBalance], amount: int, address_to: Address):
        while amount > 0:
            random_item = random.choice(wallets_with_balances)
            value = random.randint(1, min(amount, random_item.balance))
            tx = Transaction(
                address_from=random_item.wallet.address,
                address_to=address_to, value=value)
            wallet_credentials = Credentials(
                private_key=random_item.wallet.decoded_private_key)
            tx_hash = await self.blockchain_connector.execute_tx(tx, wallet_credentials)
            if tx_hash is None:
                continue
            amount -= value
            random_item.balance -= value
