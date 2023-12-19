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

def context_input_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Context Input Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


# UTXO Input

utxo_input_name = "UTXO Input"
utxo_input_fields: List[Field] = [
    input_type_field(0, utxo_input_name),
    SimpleField("Transaction ID", ByteArray(36), "The identifier of the transaction that created the referenced output."),
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
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(UTXOInput())

# Commitment Input

commitment_input_name = "Commitment Input"
commitment_input_fields: List[Field] = [
    context_input_type_field(0, commitment_input_name),
    SimpleField(
        "Commitment ID", ByteArray(36), "The commitment identifier to reference to."
    ),
]


def CommitmentInput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        commitment_input_name,
        "A Commitment Input allows referencing a commitment to a certain slot and is used to provide a notion of time for transaction execution that is linked to the containing Block's <code>Issuing Time</code>.",
        commitment_input_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(CommitmentInput())

# Block Issuance Credit Input

block_issuance_credit_input_name = "Block Issuance Credit Input"
block_issuance_credit_input_fields: List[Field] = [
    context_input_type_field(1, block_issuance_credit_input_name),
    SimpleField(
        "Account ID",
        ByteArray(32),
        "The ID of the Account for which this input provides the BIC.",
    ),
]


def BlockIssuanceCreditInput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        block_issuance_credit_input_name,
        "A Block Issuance Credit Input provides the BIC balance of a specific account as context to transaction execution.",
        block_issuance_credit_input_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(BlockIssuanceCreditInput())

# Reward Input

reward_input_name = "Reward Input"
reward_input_fields: List[Field] = [
    context_input_type_field(2, reward_input_name),
    SimpleField(
        "Index",
        UInt16(),
        "The index of the transaction input for which to claim rewards.",
    ),
]


def RewardInput(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        reward_input_name,
        "A Reward Input indicates which transaction Input is claiming Mana rewards.",
        reward_input_fields,
        tipReference=45,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(RewardInput())
