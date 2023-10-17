import copy
from typing import List
from schemas.output import output_type_field
from schemas.common import AVAILABLE_SCHEMAS, AmountField
from typedefs.datatype import ByteArray, UInt64
from typedefs.deposit_weight import DepositWeight
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import AtMostOneOfEach
from schemas.unlock_condition import (
    AddressUnlockCondition,
    UnlockConditionsCountField,
)

name = "Delegation Output"
summary = "Describes a Delegation Output, which delegates its contained IOTA tokens to a validator."
amount = copy.deepcopy(AmountField)
amount.deposit_weight = DepositWeight.Delegation

delegated_amount = SimpleField(
    "Delegated Amount",
    UInt64(),
    "The amount of delegated IOTA coins.",
    deposit_weight=DepositWeight.Delegation,
)
delegation_id = SimpleField(
    "Delegation ID",
    ByteArray(32),
    "Unique identifier of the Delegation Output, which is the BLAKE2b-256 hash of the <i>Output ID</i> that created it.",
    deposit_weight=DepositWeight.Delegation,
)
validator_address = SimpleField(
    "Validator Address",
    ByteArray(32),
    "The <i>Account Address</i> of the validator to which this output is delegating.",
    deposit_weight=DepositWeight.Delegation,
)
start_epoch = SimpleField(
    "Start Epoch",
    UInt64(),
    "The index of the first epoch for which this output delegates.",
    deposit_weight=DepositWeight.Delegation,
)
end_epoch = SimpleField(
    "End Epoch",
    UInt64(),
    "The index of the last epoch for which this output delegates.",
    deposit_weight=DepositWeight.Delegation,
)

delegation_unlock_conditions = ComplexField(
    "Unlock Conditions",
    AtMostOneOfEach(),
    [
        AddressUnlockCondition(),
    ],
)

fields: List[Field] = [
    output_type_field(4, name, deposit_weight=DepositWeight.Delegation),
    AmountField,
    delegated_amount,
    delegation_id,
    validator_address,
    start_epoch,
    end_epoch,
    UnlockConditionsCountField,
    delegation_unlock_conditions,
]


def DelegationOutput(
    omitFields: bool = False,
) -> Schema:
    return Schema(name, summary, fields, tipReference=40, omitFields=omitFields)


AVAILABLE_SCHEMAS.append(DelegationOutput())
