import web3
from web3.exceptions import TimeExhausted

from .schemas import Transaction, Credentials
from custom_types import TxHash, Address


class BlockchainConnector:
    def __init__(self, blockchain_url: str, default_gas_value: int = 3_000_000):
        provider = web3.AsyncHTTPProvider(blockchain_url)
        self.web3 = web3.AsyncWeb3(provider)
        self.default_gas_value = default_gas_value

    async def get_balance(self, address: Address) -> int:
        return await self.web3.eth.get_balance(address)

    async def get_tx(self, tx_hash: TxHash) -> Transaction | None:
        tx = await self.web3.eth.get_transaction(tx_hash)
        if tx is None:
            return None
        return Transaction(**tx)

    async def execute_tx(self, tx: Transaction, credentials: Credentials) -> TxHash | None:
        await self.fill_tx(tx)
        tx_dict = tx.to_tx_dict()
        signed_tx = self.web3.eth.account.sign_transaction(
            tx_dict, credentials.private_key)
        tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return await self._wait_for_tx_execution(tx_hash)

    async def fill_tx(self, tx: Transaction):
        if tx.chain_id is None:
            tx.chain_id = await self.web3.eth.chain_id
        if tx.nonce is None:
            tx.nonce = await self.web3.eth.get_transaction_count(tx.address_from)
        if tx.gas_price is None:
            tx.gas_price = await self.web3.eth.gas_price
        if tx.gas is None:
            tx.gas = self.default_gas_value

    async def _wait_for_tx_execution(self, tx_hash: str) -> TxHash | None:
        try:
            receipt = await self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt["transactionHash"]
        except TimeExhausted:
            return None
