from typing import List
from schemas.common import AVAILABLE_SCHEMAS
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


# Ed25519 Public Key Block Issuer Key

ed25519_public_key_block_issuer_key_name = "Ed25519 Public Key Block Issuer Key"
ed25519_public_key_block_issuer_key_description = (
    "A Block Issuer Key backed by an Ed25519 Public Key."
)
ed25519_public_key_block_issuer_key_fields: List[Field] = [
    block_issuer_key_type_field(
        0, ed25519_public_key_block_issuer_key_name, article="an"
    ),
    SimpleField(
        "Public Key",
        ByteArray(32),
        "The raw bytes of the Ed25519 public key.",
        deposit_weight=DepositWeight.BlockIssuerKey,
    ),
]


def Ed25519PublicKeyBlockIssuerKey(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        ed25519_public_key_block_issuer_key_name,
        ed25519_public_key_block_issuer_key_description,
        ed25519_public_key_block_issuer_key_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Ed25519PublicKeyBlockIssuerKey())


# Ed25519 Public Key Hash Block Issuer Key

ed25519_public_key_hash_block_issuer_key_name = (
    "Ed25519 Public Key Hash Block Issuer Key"
)
ed25519_public_key_hash_block_issuer_key_description = (
    "A block issuer key for issuing blocks from implicit accounts."
)
ed25519_public_key_hash_block_issuer_key_fields: List[Field] = [
    block_issuer_key_type_field(
        1, ed25519_public_key_hash_block_issuer_key_name, article="an"
    ),
    SimpleField(
        "PubKeyHash",
        ByteArray(32),
        "The raw bytes of the Implicit Account Creation Address which is the BLAKE2b-256 hash of the Ed25519 public key.",
        deposit_weight=DepositWeight.BlockIssuerKey,
    ),
]


def Ed25519PublicKeyHashBlockIssuerKey(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        ed25519_public_key_hash_block_issuer_key_name,
        ed25519_public_key_hash_block_issuer_key_description,
        ed25519_public_key_hash_block_issuer_key_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Ed25519PublicKeyHashBlockIssuerKey())
