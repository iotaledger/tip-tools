from typing import List
from schemas.common import AVAILABLE_SCHEMAS
from schemas.merkle_tree import LeafHash, Node, ValueHash
from typedefs.datatype import (
    ByteArray,
    UInt16,
    UInt32,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import OneOf


output_commitment_proof = ComplexField(
    "Output Commitment Proof",
    OneOf(),
    [
        Node(),
        LeafHash(),
        ValueHash(),
    ],
)

output_id_proof_name = "Output ID Proof"
output_id_proof_fields: List[Field] = [
    SimpleField("Slot", UInt32(), "The slot in which the Output was created."),
    SimpleField(
        "Output Index", UInt16(), "The index of the output in the transaction."
    ),
    SimpleField(
        "Transaction Commitment", ByteArray(32), "The commitment to the transaction."
    ),
    output_commitment_proof,
]


def OutputIDProof(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        output_id_proof_name,
        "A merkle proof that allows for cryptographic verification that an Output ID belongs to a given Output.",
        output_id_proof_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(OutputIDProof())
