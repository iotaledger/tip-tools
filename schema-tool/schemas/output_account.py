from typedefs.datatype import ByteArray, UInt32
from typedefs.field import ComplexField, Schema, SimpleField
from schemas.feature import (
    BlockIssuerFeature,
    FeaturesCountField,
    ImmutableFeaturesCountField,
    IssuerFeature,
    MetadataFeature,
    SenderFeature,
    StakingFeature,
)
from schemas.output import output_type_field
from schemas.common import AVAILABLE_SCHEMAS, AmountField, ManaField
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import UnlockConditionsCountField
from schemas.unlock_condition import AddressUnlockCondition

account_name = "Account Output"
account_summary = "Describes an account in the ledger that can be controlled by the state and governance controllers."
account_id = SimpleField(
    "Account ID",
    ByteArray(32),
    "Unique identifier of the account, which is the BLAKE2b-256 hash of the <i>Output ID</i> that created it. <i>Account Address = Account Address Type || Account ID</i>.",
)
account_foundry_counter = SimpleField(
    "Foundry Counter",
    UInt32(),
    "A counter that denotes the number of foundries created by this account.",
)
account_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        AddressUnlockCondition(),
    ],
)
account_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [
        SenderFeature(),
        MetadataFeature(),
        BlockIssuerFeature(),
        StakingFeature(),
    ],
)

account_immutable_features = ComplexField(
    "Immutable Features",
    AtMostOneOfEach(),
    [IssuerFeature(), MetadataFeature()],
)

account_fields = [
    output_type_field(1, account_name, article="an"),
    AmountField,
    ManaField,
    account_id,
    account_foundry_counter,
    UnlockConditionsCountField,
    account_unlock_conditions,
    FeaturesCountField,
    account_features,
    ImmutableFeaturesCountField,
    account_immutable_features,
]


def AccountOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        account_name,
        account_summary,
        account_fields,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(AccountOutput())
