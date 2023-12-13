from blockchain_module import BlockchainConnector
from pydantic import BaseModel
import os


class BlockchainConfig(BaseModel):
    blockchain_url: str
    default_gas_value: int = 3_000_000


def get_blockchain_config() -> BlockchainConfig:
    return BlockchainConfig(
        blockchain_url=os.environ.get("BLOCKCHAIN_URL"),
        default_gas_value=int(os.environ.get("DEFAULT_GAS_VALUE", 3_000_000))
    )


def get_blockchain_connector() -> BlockchainConnector:
    config = get_blockchain_config()
    return BlockchainConnector(config.blockchain_url, config.default_gas_value)
