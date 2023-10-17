from typing import List
from schemas.feature import (
    FeaturesCountField,
    MetadataFeature,
    NativeTokenFeature,
    SenderFeature,
    TagFeature,
)
from schemas.output import output_type_field
from schemas.common import AVAILABLE_SCHEMAS, AmountField, ManaField
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
        AddressUnlockCondition(
            includeImplicitAccountCreationAddress=True,
        ),
        StorageDepositReturnUnlockCondition(),
        TimelockUnlock(),
        ExpirationUnlockCondition(),
    ],
)
basic_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [SenderFeature(), MetadataFeature(), TagFeature(), NativeTokenFeature()],
)

basic_fields: List[Field] = [
    output_type_field(0, basic_name),
    AmountField,
    ManaField,
    UnlockConditionsCountField,
    basic_unlock_conditions,
    FeaturesCountField,
    basic_features,
]


def BasicOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        basic_name, basic_summary, basic_fields, tipReference=41, omitFields=omitFields
    )


AVAILABLE_SCHEMAS.append(BasicOutput())
