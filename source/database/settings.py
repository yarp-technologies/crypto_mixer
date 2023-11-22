import os
from pydantic import BaseModel


class DataBaseSettings(BaseModel):
    user: str
    password: str
    db_name: str
    host: str
    port: int


def get_db_settings() -> DataBaseSettings:
    return DataBaseSettings(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        db_name=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
    )
