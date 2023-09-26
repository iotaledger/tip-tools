from typing import List
from typedefs.datatype import ByteArray, UInt8
from typedefs.deposit_weight import DepositWeight
from typedefs.field import Field, Schema, SimpleField


def block_issuer_key_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Block Issuer Key Type",
        UInt8(),
        # TODO: Factor out.
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
        deposit_weight=DepositWeight.BlockIssuerKey,
    )


# Block Issuer Key Types

block_issuer_key_ed25519_public_key_name = "Ed25519 Public Key Block Issuer Key"
block_issuer_key_ed25519_public_key_fields: List[Field] = [
    block_issuer_key_type_field(0, block_issuer_key_ed25519_public_key_name, article="an"),
    SimpleField(
        "Public Key",
        ByteArray(32),
        "The raw bytes of the Ed25519 public key.",
        deposit_weight=DepositWeight.BlockIssuerKey,
    ),
]
BlockIssuerKeyEd25519PublicKey = Schema(
    block_issuer_key_ed25519_public_key_name,
    None,
    block_issuer_key_ed25519_public_key_fields,
)

block_issuer_key_ed25519_address_name = "Ed25519 Address Block Issuer Key"
block_issuer_key_ed25519_address_description = (
    "A block issuer key for issuing blocks from implicit accounts."
)
block_issuer_key_ed25519_address_fields: List[Field] = [
    block_issuer_key_type_field(1, block_issuer_key_ed25519_address_name, article="an"),
    SimpleField(
        "PubKeyHash",
        ByteArray(32),
        "The raw bytes of the Implicit Account Creation Address which is the BLAKE2b-256 hash of the Ed25519 public key.",
        deposit_weight=DepositWeight.BlockIssuerKey,
    ),
]
BlockIssuerKeyEd25519Address = Schema(
    block_issuer_key_ed25519_address_name,
    block_issuer_key_ed25519_address_description,
    block_issuer_key_ed25519_address_fields,
)
