from typing import List

from schemas.common import AVAILABLE_SCHEMAS, payload_type_field
from typedefs.datatype import (
    LengthPrefixedArray,
    UInt32,
    UInt8,
)
from typedefs.field import Field, Schema, SimpleField, TipReference

tagged_data_name = "Tagged Data"
tagged_data_fields: List[Field] = [
    payload_type_field(0, f"{tagged_data_name} Payload"),
    SimpleField(
        "Tag",
        LengthPrefixedArray(UInt8()),
        "The tag of the data.",
    ),
    SimpleField(
        "Data",
        LengthPrefixedArray(UInt32()),
        "Binary data.",
    ),
]


def TaggedData(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        tagged_data_name,
        "Data with an optional tag. It is defined in <a href='../TIP-0023/tip-0023.md#specification'>TIP-23 (Specification)</a> with the exception of the type value, which must be set to <b>value 0</b> to be compatible with this TIP.",
        tagged_data_fields,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(TaggedData())
