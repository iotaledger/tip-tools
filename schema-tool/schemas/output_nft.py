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
from schemas.common import AVAILABLE_SCHEMAS, AmountField, ManaField
from typedefs.datatype import ByteArray
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import (
    AddressUnlockCondition,
    ExpirationUnlockCondition,
    StorageDepositReturnUnlockCondition,
    TimelockUnlock,
    UnlockConditionsCountField,
)

nft_name = "NFT Output"
nft_summary = "Describes an NFT output, a globally unique token with metadata attached."

nft_id = SimpleField(
    "NFT ID",
    ByteArray(32),
    "Unique identifier of the NFT, which is the BLAKE2b-256 hash of the <i>Output ID</i> that created it. <i>NFT Address = NFT Address Type || NFT ID</i>.",
)

nft_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        AddressUnlockCondition(),
        StorageDepositReturnUnlockCondition(),
        TimelockUnlock(),
        ExpirationUnlockCondition(),
    ],
)
nft_features = ComplexField(
    "Features",
    AtMostOneOfEach(),
    [
        SenderFeature(),
        MetadataFeature(),
        TagFeature(),
    ],
)

nft_immutable_features = ComplexField(
    "Immutable Features",
    AtMostOneOfEach(),
    [
        IssuerFeature(),
        MetadataFeature(),
    ],
)

nft_fields: List[Field] = [
    output_type_field(6, nft_name),
    AmountField,
    ManaField,
    nft_id,
    UnlockConditionsCountField,
    nft_unlock_conditions,
    FeaturesCountField,
    nft_features,
    ImmutableFeaturesCountField,
    nft_immutable_features,
]


def NftOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        nft_name, nft_summary, nft_fields, tipReference=43, omitFields=omitFields
    )


AVAILABLE_SCHEMAS.append(NftOutput())
