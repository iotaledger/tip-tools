from enum import Enum
from typedefs.datatype import UInt8
from typedefs.deposit_weight import DepositWeight
from typedefs.field import SimpleField

class OutputType(Enum):
    Basic = 0
    Account = 1
    Anchor = 2
    Foundry = 3
    Nft = 4
    Delegation = 5

def output_type_field(
    output_type: OutputType,
    name: str,
    article="a",
    deposit_weight: DepositWeight = DepositWeight.Data,
) -> SimpleField:
    return SimpleField(
        "Output Type",
        UInt8(),
        f"Set to <strong>value {output_type.value}</strong> to denote {article} <i>{name}</i>.",
        deposit_weight=deposit_weight,
    )
