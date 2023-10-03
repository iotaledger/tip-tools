from typing import List
from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import ByteArray, UInt8
from typedefs.field import Field, Schema, SimpleField


def signature_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Signature Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


# Ed25519 Signature

signature_name = "Ed25519 Signature"
signature_fields: List[Field] = [
    signature_type_field(0, signature_name, article="an"),
    SimpleField(
        "Public Key",
        ByteArray(32),
        "The Ed25519 public key that verifies the signature.",
    ),
    SimpleField("Signature", ByteArray(64), "The Ed25519 signature."),
]


def Ed25519Signature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        signature_name,
        "An Ed25519 Signature",
        signature_fields,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Ed25519Signature())
