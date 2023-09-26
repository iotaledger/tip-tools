from typing import List, Optional
from schemas.feature import (
    FeaturesCountField,
    MetadataFeature,
    SenderFeature,
    TagFeature,
)
from schemas.output import output_type_field
from schemas.common import AmountField, ManaField
from schemas.native_token import NativeTokensCountField, NativeTokens
from typedefs.field import ComplexField, Field, Schema
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import (
    AddressUnlockCondition,
    AddressUnlockConditionWithImplicitAccount,
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
        AddressUnlockConditionWithImplicitAccount,
        StorageDepositReturnUnlockCondition,
        TimelockUnlock,
        ExpirationUnlockCondition,
    ],
)
basic_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [SenderFeature, MetadataFeature, TagFeature],
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

BasicOutput = Schema(basic_name, basic_summary, basic_fields)
