from typing import List

from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import ByteArray, UInt16, UInt64, UInt8
from typedefs.field import Field, Schema, SimpleField

# Allotment

allotment_name = "Allotment"
allotment_fields: List[Field] = [
    SimpleField("Account ID", ByteArray(32), "The ID of the Account to which the Mana is allotted."),
    SimpleField(
        "Mana",
        UInt64(),
        "The amount of Mana to allot.",
    ),
]


def Allotment(
    omitFields: bool = False,
) -> Schema:
    return Schema(allotment_name,
    "Allots Mana to the account identified by the contained Account ID.",
    allotment_fields, omitFields=omitFields)


AVAILABLE_SCHEMAS.append(Allotment())
