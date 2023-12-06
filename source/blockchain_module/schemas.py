from pydantic import AliasChoices, BaseModel, Field
from custom_types import Address, TxHash
from typing import Any


class Transaction(BaseModel):
    address_from: Address = Field(validation_alias=AliasChoices(
        "address_from", "from"), serialization_alias="from")
    address_to: Address = Field(validation_alias=AliasChoices(
        "address_to", "to"), serialization_alias="to")
    value: int
    chain_id: int | None = Field(None, validation_alias=AliasChoices(
        "chain_id", "chainId"), serialization_alias="chainId")
    gas_price: int | None = Field(None, validation_alias=AliasChoices(
        "gas_price", "gasPrice"), serialization_alias="gasPrice")
    hash: TxHash | None = None
    block_number: int | None = Field(None, validation_alias=AliasChoices(
        "block_number", "blockNumber"), serialization_alias="blockNumber")
    gas: int | None = None
    nonce: int | None = None

    def to_tx_dict(self) -> dict[str, Any]:
        return self.model_dump(
            exclude=("block_number", "hash"),
            exclude_none=True,
            by_alias=True,
        )


class Credentials(BaseModel):
    private_key: Address
