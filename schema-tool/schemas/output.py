from typedefs.datatype import UInt8
from typedefs.deposit_weight import DepositWeight
from typedefs.field import SimpleField


def output_type_field(
    type_value: int,
    name: str,
    article="a",
    deposit_weight: DepositWeight = DepositWeight.Data,
) -> SimpleField:
    return SimpleField(
        "Output Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
        deposit_weight=deposit_weight,
    )
