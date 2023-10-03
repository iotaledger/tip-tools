from typing import List
from schemas.common import AVAILABLE_SCHEMAS

from typedefs.datatype import ByteArray, UInt16, UInt8
from typedefs.field import Field, Schema, SimpleField


def input_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Input Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


# UTXO Input

utxo_input_name = "UTXO Input"
utxo_input_fields: List[Field] = [
    input_type_field(0, utxo_input_name),
    SimpleField("Transaction ID", ByteArray(36), "TODO"),
    SimpleField(
        "Transaction Output Index",
        UInt16(),
        "The output index of the referenced output.",
    ),
]


def UTXOInput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        utxo_input_name,
        "Describes an input which references an unspent transaction output to consume.",
        utxo_input_fields,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(UTXOInput())
