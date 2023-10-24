from typing import List
from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import (
    ByteArray,
    LengthPrefixedArray,
    UInt16,
    UInt32,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import OneOf


def merkle_hashable_type(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Merkle Hashable Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


leaf_hash_name = "Leaf Hash"


def LeafHash(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        leaf_hash_name,
        "Contains the hash of a leaf in the tree.",
        [
            merkle_hashable_type(1, leaf_hash_name),
            SimpleField("Hash", LengthPrefixedArray(UInt8()), "The hash of the leaf."),
        ],
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(LeafHash())


value_hash_name = "Value Hash"


def ValueHash(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        value_hash_name,
        "Contains the hash of the value for which the proof is being computed.",
        [
            merkle_hashable_type(2, value_hash_name),
            SimpleField("Hash", LengthPrefixedArray(UInt8()), "The hash of the value."),
        ],
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ValueHash())


node_name = "Node"
node_description = (
    "Contains the hash of the value for which the proof is being computed."
)
# Used to avoid having to recursively define the type.
node_dummy_schema = Schema(
    node_name, node_description, [], tipReference=45, omitFields=True
)
node_fields: List[Field] = [
    merkle_hashable_type(0, node_name),
    ComplexField(
        "Left",
        OneOf(),
        [node_dummy_schema, LeafHash(omitFields=True), ValueHash(omitFields=True)],
    ),
    ComplexField(
        "Right",
        OneOf(),
        [node_dummy_schema, LeafHash(omitFields=True), ValueHash(omitFields=True)],
    ),
]


def Node(
    omitFields: bool = False,
) -> Schema:
    node = Schema(
        node_name,
        "Contains the hash of the value for which the proof is being computed.",
        node_fields,
        tipReference=45,
        omitFields=omitFields,
    )

    return node


AVAILABLE_SCHEMAS.append(Node())


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
