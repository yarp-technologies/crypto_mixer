from blockchain_module import BlockchainConnector, Transaction, Credentials
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_wallets_with_balances, WalletWithBalance
import random


class InternalMixer:
    def __init__(self,
                 blockchain_connector: BlockchainConnector,
                 db_session: AsyncSession):
        self.blockchain_connector = blockchain_connector
        self.db_session = db_session

    async def mix(self):
        wallets_with_balances = await get_wallets_with_balances(self.blockchain_connector, self.db_session)
        wallets_with_balances.sort(key=lambda item: item.balance, reverse=True)
        k_richest = random.randint(1, len(wallets_with_balances) // 2)
        for k in range(k_richest):
            await self._mix_iteration(wallets_with_balances, k)

    async def _mix_iteration(self, wallets_with_balances: list[WalletWithBalance], k: int):
        address_from = wallets_with_balances[k].wallet.address
        value = wallets_with_balances[k].balance // len(wallets_with_balances)
        for i in range(k + 1, len(wallets_with_balances)):
            address_to = wallets_with_balances[i].wallet.address
            tx = Transaction(address_from=address_from,
                             address_to=address_to, value=value)
            credentials = Credentials(
                private_key=wallets_with_balances[k].wallet.decoded_private_key)
            await self.blockchain_connector.execute_tx(tx, credentials)
