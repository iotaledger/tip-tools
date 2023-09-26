from typing import List
from typedefs.datatype import UInt16, UInt64, UInt8
from typedefs.field import ComplexField, Field, Schema, SimpleField
from schemas.address import AccountAddress, Ed25519Address, NftAddress
from typedefs.subschema import OneOf


def unlock_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Unlock Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


# Account Unlock

account_unlock_name = "Account Unlock"
account_unlock_fields: List[Field] = [
    unlock_type_field(2, account_unlock_name, article="an"),
    SimpleField(
        "Account Reference Unlock Index",
        UInt16(),
        "Index of input and unlock corresponding to an Account Output.",
    ),
]
AccountUnlock = Schema(
    account_unlock_name,
    "Points to the unlock of a consumed Account Output.",
    account_unlock_fields,
)

# NFT Unlock

nft_unlock_name = "NFT Unlock"
nft_unlock_fields: List[Field] = [
    unlock_type_field(3, nft_unlock_name, article="an"),
    SimpleField(
        "NFT Reference Unlock Index",
        UInt16(),
        "Index of input and unlock corresponding to an NFT Output.",
    ),
]
AccountUnlock = Schema(
    nft_unlock_name,
    "Points to the unlock of a consumed NFT Output.",
    nft_unlock_fields,
)
