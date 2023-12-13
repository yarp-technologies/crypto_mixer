from database.models import Wallet
from custom_types import ID
from typing import Iterable, Iterator, AsyncGenerator, AsyncIterator, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class AdminPanel:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_wallet_ids(self) -> AsyncGenerator[Wallet, None]:
        async with self.session.begin():
            query = select(Wallet)
            data = await self.session.execute(query)
            for item in data.scalars():
                yield item

    async def get_wallet(self, id: ID) -> Wallet | None:
        async with self.session.begin():
            wallet = await self.session.get(Wallet, id)
            return wallet

    async def get_wallets(self, ids: Iterable[ID]) -> AsyncGenerator[Wallet, None]:
        async with self.session.begin():
            query = select(Wallet).where(Wallet.id.in_(ids))
            data = await self.session.execute(query)
            for row in data.scalars():
                yield row

    async def create_wallet(self, wallet: Wallet):
        async with self.session.begin():
            self.session.add(wallet)
            await self.session.commit()

    async def delete_wallet(self, id: ID):
        async with self.session.begin():
            wallet = await self.session.get(Wallet, id)
            if wallet is None:
                return
            await self.session.delete(wallet)
            await self.session.commit()
