from mixing_module import AdminPanel
from database import get_session
from database.models import Wallet


async def main():
    session_generator = get_session()
    session = await anext(session_generator)
    admin_panel = AdminPanel(session)
    wallet = Wallet(
        address="0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
        private_key="4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
    )
    await admin_panel.create_wallet(wallet)
    async for wallet in admin_panel.get_all_wallet_ids():
        print(wallet.address, wallet.private_key)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
