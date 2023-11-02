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
        "Data with an optional tag.",
        tagged_data_fields,
        tipReference=53,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(TaggedData())
