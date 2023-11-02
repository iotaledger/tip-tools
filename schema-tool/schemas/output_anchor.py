from typedefs.datatype import ByteArray, LengthPrefixedArray, UInt16, UInt32
from typedefs.field import ComplexField, Schema, SimpleField
from schemas.feature import (
    MAX_METADATA_LENGTH,
    FeaturesCountField,
    ImmutableFeaturesCountField,
    IssuerFeature,
    MetadataFeature,
    SenderFeature,
)
from schemas.output import OutputType, output_type_field
from schemas.common import AVAILABLE_SCHEMAS, AmountField, ManaField
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import UnlockConditionsCountField
from schemas.unlock_condition import (
    StateControllerUnlockCondition,
    GovernorUnlockCondition,
)

MIN_STATE_METADATA_LENGTH = 0
MAX_STATE_METADATA_LENGTH = MAX_METADATA_LENGTH

anchor_name = "Anchor Output"
anchor_summary = "An anchor in the ledger that can be controlled by the state and governance controllers."
anchor_id = SimpleField(
    "Anchor ID",
    ByteArray(32),
    "Unique identifier of the anchor, which is the BLAKE2b-256 hash of the <i>Output ID</i> that created it. <i>Anchor Address = Anchor Address Type || Anchor ID</i>.",
)
anchor_state_index = SimpleField(
    "State Index",
    UInt32(),
    "A counter that must increase by 1 every time the anchor is state transitioned.",
)
anchor_state_metadata = SimpleField(
    "State Metadata",
    LengthPrefixedArray(
        UInt16(),
        minLength=MIN_STATE_METADATA_LENGTH,
        maxLength=MAX_STATE_METADATA_LENGTH,
    ),
    "Metadata that can only be changed by the state controller. A leading uint16 denotes its length.",
)
anchor_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        StateControllerUnlockCondition(),
        GovernorUnlockCondition(),
    ],
)
anchor_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [
        SenderFeature(),
        MetadataFeature(),
    ],
)

anchor_immutable_features = ComplexField(
    "Immutable Features",
    AtMostOneOfEach(),
    [IssuerFeature(), MetadataFeature()],
)

anchor_fields = [
    output_type_field(OutputType.Anchor, anchor_name, article="an"),
    AmountField,
    ManaField,
    anchor_id,
    anchor_state_index,
    anchor_state_metadata,
    UnlockConditionsCountField,
    anchor_unlock_conditions,
    FeaturesCountField,
    anchor_features,
    ImmutableFeaturesCountField,
    anchor_immutable_features,
]


def AnchorOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        anchor_name,
        anchor_summary,
        anchor_fields,
        tipReference=54,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AnchorOutput())
