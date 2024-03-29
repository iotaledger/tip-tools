from typing import List
from schemas.block_issuer_key import Ed25519PublicKeyHashBlockIssuerKey
from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import (
    ByteArray,
    LengthPrefixedArray,
    UInt16,
    UInt256,
    UInt32,
    UInt64,
    UInt8,
)
from typedefs.deposit_weight import DepositWeight
from typedefs.field import ComplexField, Field, Schema, SimpleField
from schemas.address import (
    AccountAddress,
    AnchorAddress,
    Ed25519Address,
    MultiAddress,
    NftAddress,
    RestrictedAddress,
)
from typedefs.subschema import AnyOf, OneOf

MIN_METADATA_LENGTH = 1
MAX_METADATA_LENGTH = 8192
MAX_TAG_LENGTH = 255
MIN_BLOCK_ISSUER_KEYS = 1
MAX_BLOCK_ISSUER_KEYS = 128


def feature_type_field(
    type_value: int,
    name: str,
    article="a",
    deposit_weight: DepositWeight = DepositWeight.Data,
) -> SimpleField:
    return SimpleField(
        "Feature Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
        deposit_weight=deposit_weight,
    )


FeaturesCountField = SimpleField(
    "Features Count", UInt8(), "The number of features following."
)

ImmutableFeaturesCountField = SimpleField(
    "Immutable Features Count",
    UInt8(),
    "The number of immutable features following. Immutable features are defined upon deployment of the UTXO state machine and are not allowed to change in any future state transition.",
)

# Sender Feature

sender_feature_name = "Sender Feature"
sender_feature_description = "Identifies the validated sender of the output."
sender_feature_sender = ComplexField(
    "Sender",
    OneOf(),
    [
        Ed25519Address(omitFields=True),
        AccountAddress(omitFields=True),
        NftAddress(omitFields=True),
        AnchorAddress(omitFields=True),
        MultiAddress(omitFields=True),
        RestrictedAddress(omitFields=True),
    ],
)
sender_feature_fields: List[Field] = [
    feature_type_field(0, sender_feature_name),
    sender_feature_sender,
]


def SenderFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        sender_feature_name,
        sender_feature_description,
        sender_feature_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(SenderFeature())


# Issuer Feature

issuer_feature_name = "Issuer Feature"
issuer_feature_description = (
    "Identifies the validated issuer of the UTXO state machine."
)
issuer_feature_issuer = ComplexField(
    "Issuer",
    OneOf(),
    [
        Ed25519Address(omitFields=True),
        AccountAddress(omitFields=True),
        NftAddress(omitFields=True),
        AnchorAddress(omitFields=True),
        MultiAddress(omitFields=True),
        RestrictedAddress(omitFields=True),
    ],
)
issuer_feature_fields: List[Field] = [
    feature_type_field(1, issuer_feature_name),
    issuer_feature_issuer,
]


def IssuerFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        issuer_feature_name,
        issuer_feature_description,
        issuer_feature_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(IssuerFeature())

# Metadata Feature

metadata_entry_fields: List[Field] = [
    SimpleField(
        "Key",
        # Min/Max Length not set. Map defines an overall max byte size.
        LengthPrefixedArray(UInt8()),
        "A string which may only consist of printable ASCII characters. A leading uint8 denotes its length.",
    ),
    SimpleField(
        "Value",
        # Min/Max Length not set. Map defines an overall max byte size.
        LengthPrefixedArray(UInt16()),
        "An array of arbitrary binary data. A leading uint16 denotes its length.",
    ),
]


metadata_entry = Schema(
    "Metadata Entry",
    "A map entry consisting of a string key and an arbitrary byte value.",
    metadata_entry_fields,
)

metadata_feature_name = "Metadata Feature"
metadata_feature_description = (
    "Defines a map of key-value pairs that is stored in the output."
)
metadata_entries_count = SimpleField(
    "Entries Count", UInt8(), "The number of entries in the map."
)
metadata_entries = ComplexField("Entries", AnyOf(1, 255), [metadata_entry])
metadata_feature_fields: List[Field] = [
    feature_type_field(2, metadata_feature_name),
    metadata_entries_count,
    metadata_entries,
]


def MetadataFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        metadata_feature_name,
        metadata_feature_description,
        metadata_feature_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(MetadataFeature())

# State Metadata Feature

state_metadata_feature_name = "State Metadata Feature"
state_metadata_feature_description = "Defines a map of key-value pairs that is stored in the output, that can only be modified by the State Controller."

state_metadata_feature_fields: List[Field] = [
    feature_type_field(3, state_metadata_feature_name),
    metadata_entries_count,
    metadata_entries,
]


def StateMetadataFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        state_metadata_feature_name,
        state_metadata_feature_description,
        state_metadata_feature_fields,
        tipReference=54,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(StateMetadataFeature())

# Tag Feature

tag_feature_name = "Tag Feature"
tag_feature_description = "Defines an indexation tag to which the output can be indexed by additional node plugins."
tag_feature_fields: List[Field] = [
    feature_type_field(4, tag_feature_name),
    SimpleField(
        "Tag",
        LengthPrefixedArray(UInt8(), minLength=1, maxLength=MAX_TAG_LENGTH),
        "Binary indexation data. A leading uint8 denotes its length.",
    ),
]


def TagFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        tag_feature_name,
        tag_feature_description,
        tag_feature_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(TagFeature())

# Native Token Feature

native_token_feature_name = "Native Token Feature"
native_token_feature_description = (
    "A feature that carries a user-defined Native Token minted by a Foundry Output."
)
native_token_id = SimpleField(
    "Token ID",
    ByteArray(38),
    "Identifier of the native token. Its derivation is defined in <a href='../TIP-0044/tip-0044.md#foundry-output'>TIP-44 (Foundry Output)</a>.",
)
native_token_amount = SimpleField(
    "Amount", UInt256(), "Amount of native tokens of the given <i>Token ID</i>."
)
native_token_feature_fields: List[Field] = [
    feature_type_field(5, native_token_feature_name),
    native_token_id,
    native_token_amount,
]


def NativeTokenFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        native_token_feature_name,
        native_token_feature_description,
        native_token_feature_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(NativeTokenFeature())

# Block Issuer Feature

block_issuer_feature_name = "Block Issuer Feature"
block_issuer_feature_description = (
    "Contains the keys with which the account can create block signatures."
)
block_issuer_feature_expiry_slot = SimpleField(
    "Expiry Slot",
    UInt32(),
    "The slot index at which the <i>Block Issuer Feature</i> expires and can be removed.",
)
block_issuer_feature_keys_count = SimpleField(
    "Block Issuer Keys Count", UInt8(), "The number of Block Issuer Keys."
)
block_issuer_feature_keys = ComplexField(
    "Block Issuer Keys",
    AnyOf(MIN_BLOCK_ISSUER_KEYS, MAX_BLOCK_ISSUER_KEYS),
    [Ed25519PublicKeyHashBlockIssuerKey()],
)

block_issuer_feature_fields: List[Field] = [
    feature_type_field(6, block_issuer_feature_name),
    block_issuer_feature_expiry_slot,
    block_issuer_feature_keys_count,
    block_issuer_feature_keys,
]


def BlockIssuerFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        block_issuer_feature_name,
        block_issuer_feature_description,
        block_issuer_feature_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(BlockIssuerFeature())

# Staking Feature

staking_feature_name = "Staking Feature"
staking_feature_description = "Stakes IOTA coins to become eligible for committee selection, validate the network and receive Mana rewards."
staking_feature_fields: List[Field] = [
    feature_type_field(7, staking_feature_name, deposit_weight=DepositWeight.Staking),
    SimpleField(
        "Staked Amount",
        UInt64(),
        "The amount of IOTA coins that are locked and staked in the containing account.",
        deposit_weight=DepositWeight.Staking,
    ),
    SimpleField(
        "Fixed Cost",
        UInt64(),
        "The fixed cost of the validator, which it receives as part of its Mana rewards.",
        deposit_weight=DepositWeight.Staking,
    ),
    SimpleField(
        "Start Epoch",
        UInt64(),
        "The epoch index in which the staking started.",
        deposit_weight=DepositWeight.Staking,
    ),
    SimpleField(
        "End Epoch",
        UInt64(),
        "The epoch index in which the staking ends.",
        deposit_weight=DepositWeight.Staking,
    ),
]


def StakingFeature(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        staking_feature_name,
        staking_feature_description,
        staking_feature_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(StakingFeature())
