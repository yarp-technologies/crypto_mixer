from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from pydantic import PostgresDsn
from typing import AsyncIterator

from .settings import get_db_settings

Base = declarative_base()

DB_SCHEME = "postgresql+asyncpg"
DB_SETTINGS = get_db_settings()

DATABASE_URI = PostgresDsn.build(
    scheme=DB_SCHEME,
    username=DB_SETTINGS.user,
    password=DB_SETTINGS.password,
    host=DB_SETTINGS.host,
    port=DB_SETTINGS.port,
    path=DB_SETTINGS.db_name,
)

ENGINE = create_async_engine(str(DATABASE_URI))


async def get_session() -> AsyncIterator[AsyncSession]:
    session = sessionmaker(
        bind=ENGINE,
        class_=AsyncSession,
    )
    async with session() as connection:
        yield connection
