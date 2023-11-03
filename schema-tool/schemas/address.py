from enum import Enum
from typing import List

from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import (
    ByteArray,
    LengthPrefixedArray,
    UInt16,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import AnyOf, OneOf

MIN_MULTI_ADDRESSES = 1
MAX_MULTI_ADDRESSES = 10


class AddressType(Enum):
    Ed25519 = 0
    Account = 8
    Nft = 16
    Anchor = 24
    ImplicitAccountCreation = 32
    Multi = 40
    Restricted = 48


def address_type_field(
    address_type: AddressType, name: str, article="a"
) -> SimpleField:
    return SimpleField(
        "Address Type",
        UInt8(),
        f"Set to <strong>value {address_type.value}</strong> to denote {article} <i>{name}</i>.",
    )


# Ed25519 Address

address_ed25519_name = "Ed25519 Address"
address_ed25519_description = "An Address derived from an Ed25519 Public Key."
address_ed25519_pubkeyhash = SimpleField(
    "PubKeyHash",
    ByteArray(32),
    "The raw bytes of the Ed25519 address which is the BLAKE2b-256 hash of the Ed25519 public key.",
)
address_ed25519_fields: List[Field] = [
    address_type_field(AddressType.Ed25519, address_ed25519_name, article="an"),
    address_ed25519_pubkeyhash,
]


def Ed25519Address(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_ed25519_name,
        address_ed25519_description,
        address_ed25519_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Ed25519Address())


# Account Address

address_account_name = "Account Address"
address_account_description = "An Address derived from an Account ID which can be unlocked by unlocking the corresponding Account."
address_account_id = SimpleField(
    "Account ID",
    ByteArray(32),
    "The raw bytes of the <i>Account ID</i> which is the BLAKE2b-256 hash of the Output ID that created it.",
)
address_account_fields: List[Field] = [
    address_type_field(AddressType.Account, address_account_name, article="an"),
    address_account_id,
]


def AccountAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_account_name,
        address_account_description,
        address_account_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AccountAddress())


# NFT Address

address_nft_name = "NFT Address"
address_nft_description = "An Address derived from an NFT ID which can be unlocked by unlocking the corresponding NFT."
address_nft_id = SimpleField(
    "NFT ID",
    ByteArray(32),
    "The raw bytes of the <i>NFT ID</i> which is the BLAKE2b-256 hash of the Output ID that created it.",
)
address_nft_fields: List[Field] = [
    address_type_field(AddressType.Nft, address_nft_name, article="an"),
    address_nft_id,
]


def NftAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_nft_name,
        address_nft_description,
        address_nft_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(NftAddress())


# Anchor Address

address_anchor_name = "Anchor Address"
address_anchor_description = "An Address derived from an Anchor ID which can be unlocked by unlocking the corresponding Anchor."
address_anchor_id = SimpleField(
    "Anchor ID",
    ByteArray(32),
    "The raw bytes of the <i>Anchor ID</i> which is the BLAKE2b-256 hash of the Output ID that created it.",
)
address_anchor_fields: List[Field] = [
    address_type_field(AddressType.Anchor, address_anchor_name, article="an"),
    address_anchor_id,
]


def AnchorAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_anchor_name,
        address_anchor_description,
        address_anchor_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AnchorAddress())


# Implicit Account Creation Address

address_implicit_account_creation_name = "Implicit Account Creation Address"
address_implicit_account_creation_description = "Defines an address on which an <i>Implicit Account</i> is created when it receives a Basic Output."
address_implicit_account_creation_pubkeyhash = SimpleField(
    "PubKeyHash",
    ByteArray(32),
    "The raw bytes of the Implicit Account Creation Address which is the BLAKE2b-256 hash of the Ed25519 public key.",
)
address_implicit_account_creation_fields: List[Field] = [
    address_type_field(
        AddressType.ImplicitAccountCreation,
        address_implicit_account_creation_name,
        article="an",
    ),
    address_implicit_account_creation_pubkeyhash,
]


def ImplicitAccountCreationAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_implicit_account_creation_name,
        address_implicit_account_creation_description,
        address_implicit_account_creation_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ImplicitAccountCreationAddress())


# Multi Address

address_multi_name = "Multi Address"
address_multi_description = "Defines a Multi Address that consists of addresses with weights and a threshold value. The Multi Address can be unlocked if the cumulative weight of all unlocked addresses is equal to or exceeds the threshold."
weight = SimpleField("Weight", UInt8(), "The weight of the unlocked address.")
address_multi_nested_addresses = ComplexField(
    "Address",
    OneOf(),
    [
        Ed25519Address(omitFields=True),
        AccountAddress(omitFields=True),
        NftAddress(omitFields=True),
    ],
)
address_weighted = Schema(
    "Weighted Address",
    "An Address with an assigned weight.",
    [address_multi_nested_addresses, weight],
)
address_multi_address_count = SimpleField(
    "Addresses Count", UInt8(), "The number of addresses following."
)
address_multi_addresses = ComplexField(
    "Addresses", AnyOf(MIN_MULTI_ADDRESSES, MAX_MULTI_ADDRESSES), [address_weighted]
)
address_multi_threshold = SimpleField(
    "Threshold",
    UInt16(),
    "The threshold that needs to be reached by the unlocked addresses in order to unlock the Multi Address.",
)
address_multi_fields: List[Field] = [
    address_type_field(AddressType.Multi, address_multi_name, article="a"),
    address_multi_address_count,
    address_multi_addresses,
    address_multi_threshold,
]


def MultiAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_multi_name,
        address_multi_description,
        address_multi_fields,
        tipReference=52,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(MultiAddress())

# Restricted Address

address_restricted_name = "Restricted Address"
address_restricted_description = "An address that contains another address and allows for configuring its capabilities."
address_restricted_capabilities = SimpleField(
    "Allowed Capabilities",
    LengthPrefixedArray(UInt8(), minLength=0, maxLength=1),
    "Bitflags expressed as a series of bytes. A leading <code>uint8</code> denotes its length.",
)
address_restricted_nested_addresses = ComplexField(
    "Address",
    OneOf(),
    [
        Ed25519Address(omitFields=True),
        AccountAddress(omitFields=True),
        NftAddress(omitFields=True),
        AnchorAddress(omitFields=True),
        MultiAddress(omitFields=True),
    ],
)
address_restricted_fields: List[Field] = [
    address_type_field(AddressType.Restricted, address_restricted_name, article="a"),
    address_restricted_nested_addresses,
    address_restricted_capabilities,
]


def RestrictedAddress(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        address_restricted_name,
        address_restricted_description,
        address_restricted_fields,
        tipReference=50,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(RestrictedAddress())
