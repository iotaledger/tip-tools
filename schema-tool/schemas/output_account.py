from typedefs.datatype import ByteArray, LengthPrefixedArray, UInt16, UInt32
from typedefs.field import ComplexField, Schema, SimpleField
from schemas.feature import (
    MAX_METADATA_LENGTH,
    BlockIssuerFeature,
    FeaturesCountField,
    ImmutableFeaturesCountField,
    IssuerFeature,
    MetadataFeature,
    SenderFeature,
    StakingFeature,
)
from schemas.output import output_type_field
from schemas.common import AmountField, ManaField
from schemas.native_token import NativeTokensCountField, NativeTokens
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import UnlockConditionsCountField
from schemas.unlock_condition import (
    StateControllerUnlockCondition,
    GovernorUnlockCondition,
)

MIN_STATE_METADATA_LENGTH = 0
MAX_STATE_METADATA_LENGTH = MAX_METADATA_LENGTH

account_name = "Account Output"
account_summary = "Describes an account in the ledger that can be controlled by the state and governance controllers."
account_id = SimpleField(
    "Account ID",
    ByteArray(32),
    "Unique identifier of the account, which is the BLAKE2b-256 hash of the <i>Output ID</i> that created it. <i>Account Address = Account Address Type || Account ID</i>.",
)
account_state_index = SimpleField(
    "State Index",
    UInt32(),
    "A counter that must increase by 1 every time the account is state transitioned.",
)
account_state_metadata = SimpleField(
    "State Metadata",
    LengthPrefixedArray(
        UInt16(), minLength=MIN_STATE_METADATA_LENGTH, maxLength=MAX_STATE_METADATA_LENGTH
    ),
    "Metadata that can only be changed by the state controller. A leading uint16 denotes its length.",
)
account_foundry_counter = SimpleField(
    "Foundry Counter",
    UInt32(),
    "A counter that denotes the number of foundries created by this account.",
)
account_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [StateControllerUnlockCondition, GovernorUnlockCondition],
)
account_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [SenderFeature, MetadataFeature, BlockIssuerFeature, StakingFeature],
)

account_immutable_features = ComplexField(
    "Immutable Features",
    AtMostOneOfEach(),
    [IssuerFeature, MetadataFeature],
)

account_fields = [
    output_type_field(4, account_name, article="an"),
    AmountField,
    ManaField,
    NativeTokensCountField,
    NativeTokens,
    account_id,
    account_state_index,
    account_state_metadata,
    account_foundry_counter,
    UnlockConditionsCountField,
    account_unlock_conditions,
    FeaturesCountField,
    account_features,
    ImmutableFeaturesCountField,
    account_immutable_features,
]

AccountOutput = Schema(account_name, account_summary, account_fields)
