from .internal_mixer import InternalMixer
from database import get_session
from blockchain_module import BlockchainConnector
import asyncio


class MixingService:
    def __init__(self, blockchain_connector: BlockchainConnector,
                 mixing_interval: float = 5 * 60.0):
        self.blockchain_connector = blockchain_connector
        self.mixing_interval = mixing_interval

    async def working_loop(self):
        while True:
            session_generator = get_session()
            session = await anext(session_generator)
            mixer = InternalMixer(self.blockchain_connector, session)
            await mixer.mix()
            await asyncio.sleep(self.mixing_interval)
