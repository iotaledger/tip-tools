from typing import List
from typedefs.datatype import ByteArray, UInt64, UInt8
from typedefs.deposit_weight import DepositWeight
from typedefs.field import Field, Schema, SimpleField

AVAILABLE_SCHEMAS = []


def payload_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Payload Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


AmountField = SimpleField(
    "Amount", UInt64(), "The amount of IOTA coins held by the output."
)
ManaField = SimpleField(
    "Mana", UInt64(), "The amount of Stored Mana held by the output."
)

offset_output_id = SimpleField(
    "OutputID",
    ByteArray(34),
    "The ID of the output.",
    deposit_weight=DepositWeight.Key,
)
offset_output_block_id = SimpleField(
    "Block ID (included)",
    ByteArray(40),
    "The ID of the block in which the transaction payload that created this output was included.",
)
offset_output_slot_booked = SimpleField(
    "Slot Booked",
    UInt64(),
    "The index of the slot in which the transaction that created it was booked.",
)
offset_output_slot_created = SimpleField(
    "Slot Created",
    UInt64(),
    "The index of the slot in which the transaction was created.",
)
offset_fields: List[Field] = [
    offset_output_id,
    offset_output_block_id,
    offset_output_slot_booked,
    offset_output_slot_created,
]
OutputOffset = Schema("Offset", "The storage offset for every output.", offset_fields)
