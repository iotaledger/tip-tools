from typing import List
from typedefs.datatype import (
    ByteArray,
    LengthPrefixedByteArray,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import AnyOf, OneOf


def address_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Address Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )

# Ed25519 Address

address_ed25519_name = "Ed25519 Address"
address_ed25519_pubkeyhash = SimpleField(
    "PubKeyHash",
    ByteArray(32),
    "The raw bytes of the Ed25519 address which is the BLAKE2b-256 hash of the Ed25519 public key.",
)
address_ed25519_fields: List[Field] = [
    address_type_field(0, address_ed25519_name, article="an"),
    address_ed25519_pubkeyhash,
]
Ed25519Address = Schema(address_ed25519_name, None, address_ed25519_fields)

# Account Address

address_account_name = "Account Address"
address_account_id = SimpleField(
    "Account ID",
    ByteArray(32),
    "The raw bytes of the <i>Account ID</i> which is the BLAKE2b-256 hash of the Output ID that created it.",
)
address_account_fields: List[Field] = [
    address_type_field(8, address_account_name, article="an"),
    address_account_id,
]
AccountAddress = Schema(address_account_name, None, address_account_fields)

# NFT Address

address_nft_name = "NFT Address"
address_nft_id = SimpleField(
    "NFT ID",
    ByteArray(32),
    "The raw bytes of the <i>NFT ID</i> which is the BLAKE2b-256 hash of the Output ID that created it.",
)
address_nft_fields: List[Field] = [
    address_type_field(16, address_nft_name, article="an"),
    address_nft_id,
]
NftAddress = Schema(address_nft_name, None, address_nft_fields)

# Implicit Account Creation Address

address_implicit_account_creation_name = "Implicit Account Creation Address"
address_implicit_account_creation_description = "Defines an address on which an <i>Implicit Account</i> is created when it receives a Basic Output."
address_implicit_account_creation_pubkeyhash = SimpleField(
    "PubKeyHash",
    ByteArray(32),
    "The raw bytes of the Implicit Account Creation Address which is the BLAKE2b-256 hash of the Ed25519 public key.",
)
address_implicit_account_creation_fields: List[Field] = [
    address_type_field(24, address_implicit_account_creation_name, article="an"),
    address_implicit_account_creation_pubkeyhash
]
ImplicitAccountCreationAddress = Schema(
    address_implicit_account_creation_name,
    address_implicit_account_creation_description,
    address_implicit_account_creation_fields,
)

# Multi Address

address_multi_name = "Multi Address"
address_multi_description = "Defines a Multi Address that consists of addresses with weights and a threshold value. The Multi Address can be unlocked if the cumulative weight of all unlocked addresses is equal to or exceeds the threshold."
weight = SimpleField("Weight", UInt8(), "The weight of the unlocked address.")
address_multi_nested_addresses = ComplexField(
    "Address", OneOf(), [Ed25519Address, AccountAddress, NftAddress]
)
address_with_weight = Schema(
    "Address with Weight", None, [address_multi_nested_addresses, weight]
)
address_multi_addresses = ComplexField("Addresses", AnyOf(1, 10), [address_with_weight])
address_multi_fields: List[Field] = [
    address_type_field(32, address_multi_name, article="a"),
    address_multi_addresses,
]
MultiAddress = Schema(address_multi_name, None, address_multi_fields)

# Restricted Address

address_restricted_name = "Restricted Address"
address_restricted_description = "Defines a container for other addresses which can restrict the capabilities of the underlying address."
address_restricted_capabilities = SimpleField(
    "Allowed Capabilities",
    LengthPrefixedByteArray(UInt8(), 0, 1),
    "Bitflags expressed as a series of bytes. A leading <code>uint8</code> denotes its length.",
)
address_restricted_nested_addresses = ComplexField(
    "Address", OneOf(), [Ed25519Address, AccountAddress, NftAddress, MultiAddress]
)
address_restricted_fields: List[Field] = [
    address_type_field(40, address_restricted_name, article="a"),
    address_restricted_nested_addresses,
    address_restricted_capabilities,
]
RestrictedAddress = Schema(address_restricted_name, None, address_restricted_fields)
