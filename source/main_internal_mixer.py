from blockchain_config import get_blockchain_connector
from internal_mixer import MixingService
import asyncio


async def main():
    blockchain_connector = get_blockchain_connector()
    mixing_service = MixingService(blockchain_connector)
    await mixing_service.working_loop()

if __name__ == '__main__':
    asyncio.run(main())
