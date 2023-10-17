from typing import List

from schemas.common import AVAILABLE_SCHEMAS, payload_type_field
from schemas.output_basic import BasicOutput
from schemas.output_account import AccountOutput
from schemas.output_delegation import DelegationOutput
from schemas.output_nft import NftOutput
from schemas.output_foundry import FoundryOutput
from schemas.unlock import (
    SignatureUnlock,
    MultiUnlock,
    AccountUnlock,
    NFTUnlock,
    ReferenceUnlock,
)
from schemas.tagged_data import TaggedData
from schemas.allotment import Allotment
from schemas.input import UTXOInput, BlockIssuanceCreditInput, CommitmentInput, RewardInput
from typedefs.subschema import AnyOf, Embedded, OptAnyOf, OptOneOf
from typedefs.datatype import LengthPrefixedArray, UInt16, UInt32, UInt64, UInt8
from typedefs.field import ComplexField, Field, Schema, SimpleField

MIN_INPUTS_COUNT = 1
MAX_INPUTS_COUNT = 128
MIN_OUTPUTS_COUNT = 1
MAX_OUTPUTS_COUNT = 128
MAX_ALLOTMENTS_COUNT = 128

transaction_name = "Transaction"
transaction_fields: List[Field] = [
    SimpleField(
        "Network ID",
        UInt64(),
        "The ID of the network for which this essence is valid for. It consists of the first 8 bytes of the BLAKE2b-256 hash of the <code>Network Name</code>.",
    ),
    SimpleField(
        "Creation Slot",
        UInt32(),
        "The slot index in which the transaction was created.",
    ),
    SimpleField(
        "Context Inputs Count", UInt16(), "The number of Context Inputs following."
    ),
    ComplexField(
        "Context Inputs",
        OptAnyOf(maxLength=MAX_INPUTS_COUNT),
        [CommitmentInput(), BlockIssuanceCreditInput(), RewardInput()],
    ),
    SimpleField("Inputs Count", UInt16(), "The number of Inputs following."),
    ComplexField(
        "Inputs",
        AnyOf(minLength=MIN_INPUTS_COUNT, maxLength=MAX_INPUTS_COUNT),
        [UTXOInput()],
    ),
    SimpleField("Allotments Count", UInt16(), "The number of Allotments following."),
    ComplexField(
        "Allotments",
        OptAnyOf(maxLength=MAX_ALLOTMENTS_COUNT),
        [Allotment()],
    ),
    SimpleField(
      "Capabilities",
      LengthPrefixedArray(UInt8(), minLength=0, maxLength=1),
      "The capabilities of the transaction.",
    ),
    SimpleField(
        "Payload Length", UInt32(), "The length in bytes of the optional payload."
    ),
    ComplexField(
        "Payload",
        OptOneOf(),
        [TaggedData(omitFields=True)],
    ),
    SimpleField("Outputs Count", UInt16(), "The number of Outputs following,"),
    ComplexField(
        "Outputs",
        AnyOf(MIN_OUTPUTS_COUNT, MAX_OUTPUTS_COUNT),
        [
            BasicOutput(omitFields=True),
            FoundryOutput(omitFields=True),
            AccountOutput(omitFields=True),
            NftOutput(omitFields=True),
            DelegationOutput(omitFields=True),
        ],
    ),
]

def Transaction(
    omitFields: bool = False,
    detailsOpen: bool = False,
) -> Schema:
    return Schema(
        transaction_name,
        "A transaction.",
        transaction_fields,
        omitFields=omitFields,
        detailsOpen=detailsOpen,
    )


AVAILABLE_SCHEMAS.append(Transaction())


signed_transaction_name = "Signed Transaction"
signed_transaction_fields: List[Field] = [
    payload_type_field(1, signed_transaction_name),
    ComplexField("Transaction", Embedded(), [Transaction(detailsOpen=True)]),
    SimpleField("Unlocks Count", UInt16(), "The number of unlocks following."),
    ComplexField(
        "Unlocks",
        AnyOf(MIN_INPUTS_COUNT, MAX_INPUTS_COUNT),
        [
            SignatureUnlock(omitFields=True),
            ReferenceUnlock(omitFields=True),
            AccountUnlock(omitFields=True),
            NFTUnlock(omitFields=True),
            MultiUnlock(omitFields=True),
        ],
    ),
]


def SignedTransaction(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        signed_transaction_name,
        "A transaction with its unlocks.",
        signed_transaction_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(SignedTransaction())
