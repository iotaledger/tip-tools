from typing import List
from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import (
    LengthPrefixedArray,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import OneOf


def merkle_tree_component_type(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Merkle Tree Component Type",
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
            merkle_tree_component_type(1, leaf_hash_name),
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
            merkle_tree_component_type(2, value_hash_name),
            SimpleField("Hash", LengthPrefixedArray(UInt8()), "The hash of the value."),
        ],
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ValueHash())


node_name = "Node"
node_description = (
    "A merkle tree node that contains two child components."
)
# Used to avoid having to recursively define the type.
node_dummy_schema = Schema(
    node_name, node_description, [], tipReference=45, omitFields=True
)
node_fields: List[Field] = [
    merkle_tree_component_type(0, node_name),
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
        node_description,
        node_fields,
        tipReference=45,
        omitFields=omitFields,
    )

    return node


AVAILABLE_SCHEMAS.append(Node())

