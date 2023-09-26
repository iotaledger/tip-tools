from typing import List
from schemas.feature import (
    FeaturesCountField,
    ImmutableFeaturesCountField,
    IssuerFeature,
    MetadataFeature,
    SenderFeature,
    TagFeature,
)
from schemas.output import output_type_field
from schemas.common import AmountField, ManaField
from schemas.native_token import NativeTokensCountField, NativeTokens
from typedefs.datatype import ByteArray, UInt256, UInt32, UInt8
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import AtMostOneOfEach, OneOf
from schemas.unlock_condition import (
    AddressUnlockCondition,
    ExpirationUnlockCondition,
    ImmutableAccountAddressUnlockCondition,
    StorageDepositReturnUnlockCondition,
    TimelockUnlock,
    UnlockConditionsCountField,
)


def simple_token_scheme_type_field(
    type_value: int, name: str, article="a"
) -> SimpleField:
    return SimpleField(
        "Token Scheme Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


simple_token_scheme_name = "Simple Token Scheme"
simple_token_scheme_minted_tokens = SimpleField(
    "Minted Tokens", UInt256(), "Amount of tokens minted by this foundry."
)
simple_token_scheme_melted_tokens = SimpleField(
    "Melted Tokens", UInt256(), "Amount of tokens melted by this foundry."
)
simple_token_scheme_maximum_supply = SimpleField(
    "Maximum Supply", UInt256(), "Maximum supply of tokens controlled by this foundry."
)
simple_token_scheme_fields: List[Field] = [
    simple_token_scheme_type_field(0, simple_token_scheme_name),
    simple_token_scheme_minted_tokens,
    simple_token_scheme_melted_tokens,
    simple_token_scheme_maximum_supply,
]
SimpleTokenScheme = Schema(simple_token_scheme_name, None, simple_token_scheme_fields)

foundry_name = "Foundry Output"
foundry_summary = "Describes a foundry output that is controlled by an account."

foundry_serial = SimpleField(
    "Serial Number",
    UInt32(),
    "The serial number of the foundry with respect to the controlling account.",
)

foundry_token_scheme = ComplexField(
    "Token Scheme",
    OneOf(),
    [SimpleTokenScheme],
)

foundry_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        ImmutableAccountAddressUnlockCondition,
    ],
)
foundry_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [MetadataFeature],
)

foundry_immutable_features = ComplexField(
    "Immutable Features",
    AtMostOneOfEach(),
    [MetadataFeature],
)

foundry_fields: List[Field] = [
    output_type_field(5, foundry_name),
    AmountField,
    NativeTokensCountField,
    NativeTokens,
    foundry_serial,
    foundry_token_scheme,
    UnlockConditionsCountField,
    foundry_unlock_conditions,
    FeaturesCountField,
    foundry_features,
    ImmutableFeaturesCountField,
    foundry_immutable_features,
]

NftOutput = Schema(foundry_name, foundry_summary, foundry_fields)