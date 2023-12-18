from enum import Enum
from typing import List
from schemas.common import AVAILABLE_SCHEMAS

from schemas.signature import Ed25519Signature
from typedefs.datatype import UInt16, UInt8
from typedefs.field import ComplexField, Field, Schema, SimpleField
from schemas.address import MAX_MULTI_ADDRESSES, MIN_MULTI_ADDRESSES
from typedefs.subschema import AnyOf, OneOf


class UnlockType(Enum):
    Signature = 0
    Reference = 1
    Account = 2
    Anchor = 3
    Nft = 4
    Multi = 5
    Empty = 6

def unlock_type_field(unlock_type: UnlockType, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Unlock Type",
        UInt8(),
        f"Set to <strong>value {unlock_type.value}</strong> to denote {article} <i>{name}</i>.",
    )


# Signature Unlock

signature_unlock_name = "Signature Unlock"
signature_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Signature, signature_unlock_name),
    ComplexField("Signature", OneOf(), [Ed25519Signature()]),
]


def SignatureUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        signature_unlock_name,
        "Unlocks the address derived from the contained Public Key in the transaction in which it is contained in.",
        signature_unlock_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(SignatureUnlock())

# Reference Unlock

reference_unlock_name = "Reference Unlock"
reference_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Reference, reference_unlock_name),
    SimpleField("Reference", UInt16(), "Represents the index of a previous unlock."),
]


def ReferenceUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        reference_unlock_name,
        "References a previous unlock to support unlocking multiple inputs owned by the same address.",
        reference_unlock_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ReferenceUnlock())

# Account Unlock

account_unlock_name = "Account Unlock"
account_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Account, account_unlock_name, article="an"),
    SimpleField(
        "Account Reference Unlock Index",
        UInt16(),
        "Index of input and unlock corresponding to an Account Output.",
    ),
]


def AccountUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        account_unlock_name,
        "Points to the unlock of a consumed Account Output.",
        account_unlock_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AccountUnlock())

# Anchor Unlock

anchor_unlock_name = "Anchor Unlock"
anchor_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Anchor, anchor_unlock_name, article="an"),
    SimpleField(
        "Anchor Reference Unlock Index",
        UInt16(),
        "Index of input and unlock corresponding to an Anchor Output.",
    ),
]


def AnchorUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        anchor_unlock_name,
        "Points to the unlock of a consumed Anchor Output.",
        anchor_unlock_fields,
        tipReference=54,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AnchorUnlock())

# NFT Unlock

nft_unlock_name = "NFT Unlock"
nft_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Nft, nft_unlock_name, article="an"),
    SimpleField(
        "NFT Reference Unlock Index",
        UInt16(),
        "Index of input and unlock corresponding to an NFT Output.",
    ),
]


def NFTUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        nft_unlock_name,
        "Points to the unlock of a consumed NFT Output.",
        nft_unlock_fields,
        tipReference=43,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(NFTUnlock())

# Empty Unlock

empty_unlock_name = "Empty Unlock"
empty_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Empty, empty_unlock_name, article="an"),
]


def EmptyUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        empty_unlock_name,
        "Used to maintain correct index relationship between addresses and signatures when unlocking a Multi Address where not all addresses are unlocked.",
        empty_unlock_fields,
        tipReference=52,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(EmptyUnlock())

# Multi Unlock

multi_unlock_name = "Multi Unlock"
multi_unlock_fields: List[Field] = [
    unlock_type_field(UnlockType.Multi, multi_unlock_name),
    SimpleField("Unlocks Count", UInt8(), "The number of unlocks following."),
    ComplexField(
        "Unlocks",
        AnyOf(MIN_MULTI_ADDRESSES, MAX_MULTI_ADDRESSES),
        [
            SignatureUnlock(omitFields=True),
            ReferenceUnlock(omitFields=True),
            AccountUnlock(omitFields=True),
            AnchorUnlock(omitFields=True),
            NFTUnlock(omitFields=True),
            EmptyUnlock(omitFields=True),
        ],
    ),
]


def MultiUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        multi_unlock_name,
        "Unlocks a Multi Address with a list of other unlocks.",
        multi_unlock_fields,
        tipReference=52,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(MultiUnlock())
