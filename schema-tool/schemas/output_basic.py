from typing import List, Optional
from schemas.feature import (
    FeaturesCountField,
    MetadataFeature,
    SenderFeature,
    TagFeature,
)
from schemas.output import output_type_field
from schemas.common import AVAILABLE_SCHEMAS, AmountField, ManaField
from schemas.native_token import NativeTokensCountField, NativeTokens
from typedefs.field import ComplexField, Field, Schema
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import (
    AddressUnlockCondition,
    ExpirationUnlockCondition,
    StorageDepositReturnUnlockCondition,
    TimelockUnlock,
    UnlockConditionsCountField,
)

basic_name = "Basic Output"
basic_summary = "Describes a basic output with optional features."
basic_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        AddressUnlockCondition(includeImplicitAccountCreationAddress=True, omitFields=True),
        StorageDepositReturnUnlockCondition(omitFields=True),
        TimelockUnlock(omitFields=True),
        ExpirationUnlockCondition(omitFields=True),
    ],
)
basic_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [
        SenderFeature(omitFields=True),
        MetadataFeature(omitFields=True),
        TagFeature(omitFields=True)
    ],
)

basic_fields: List[Field] = [
    output_type_field(3, basic_name),
    AmountField,
    ManaField,
    NativeTokensCountField,
    NativeTokens,
    UnlockConditionsCountField,
    basic_unlock_conditions,
    FeaturesCountField,
    basic_features,
]


def BasicOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(basic_name, basic_summary, basic_fields, omitFields=omitFields)


AVAILABLE_SCHEMAS.append(BasicOutput())
