from typing import List
from schemas.common import AVAILABLE_SCHEMAS
from typedefs.datatype import UInt64, UInt8
from typedefs.field import ComplexField, Field, Schema, SimpleField
from schemas.address import (
    AccountAddress,
    Ed25519Address,
    ImplicitAccountCreationAddress,
    MultiAddress,
    NftAddress,
    RestrictedAddress,
)
from typedefs.subschema import OneOf


def unlock_condition_type_field(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Unlock Condition Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


UnlockConditionsCountField = SimpleField(
    "Unlock Conditions Count", UInt8(), "The number of unlock conditions following."
)

regular_addresses_plus_multi_and_restricted: List[Schema] = [
    Ed25519Address(omitFields=True),
    AccountAddress(omitFields=True),
    NftAddress(omitFields=True),
    MultiAddress(omitFields=True),
    RestrictedAddress(omitFields=True),
]

regular_addresses_plus_multi_and_restricted_and_implicit_account: List[Schema] = [
    Ed25519Address(omitFields=True),
    AccountAddress(omitFields=True),
    NftAddress(omitFields=True),
    MultiAddress(omitFields=True),
    RestrictedAddress(omitFields=True),
    ImplicitAccountCreationAddress(omitFields=True),
]

# Address Unlock Condition

address_unlock_condition_name = "Address Unlock Condition"
address_unlock_condition_description = "Defines the Address that owns this output. It can unlock the output with the proper <i>Unlock</i> in a transaction."
address_unlock_condition_type = unlock_condition_type_field(
    0, address_unlock_condition_name, article="an"
)


def AddressUnlockCondition(
    omitFields: bool = False, includeImplicitAccountCreationAddress: bool = False
) -> Schema:
    address_schema = regular_addresses_plus_multi_and_restricted
    if includeImplicitAccountCreationAddress:
        address_schema = (
            regular_addresses_plus_multi_and_restricted_and_implicit_account
        )

    return Schema(
        address_unlock_condition_name,
        address_unlock_condition_description,
        [
            address_unlock_condition_type,
            ComplexField("Address", OneOf(), address_schema),
        ],
        mandatory=True,
        omitFields=omitFields,
        tipReference=38,
    )


AVAILABLE_SCHEMAS.append(AddressUnlockCondition())


# Storage Deposit Return Unlock Condition

storage_deposit_return_unlock_condition_name = "Storage Deposit Return Unlock Condition"
storage_deposit_return_unlock_condition_description = "Defines the amount of IOTAs used as storage deposit that have to be returned to <i>Return Address</i>."
storage_deposit_return_unlock_condition_return_address = ComplexField(
    "Return Address", OneOf(), regular_addresses_plus_multi_and_restricted
)
storage_deposit_return_unlock_condition_return_amount = SimpleField(
    "Return Amount",
    UInt64(),
    "Amount of IOTA coins the consuming transaction should deposit to the address defined in <i>Return Address</i>.",
)
storage_deposit_return_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(1, storage_deposit_return_unlock_condition_name),
    storage_deposit_return_unlock_condition_return_address,
    storage_deposit_return_unlock_condition_return_amount,
]


def StorageDepositReturnUnlockCondition(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        storage_deposit_return_unlock_condition_name,
        storage_deposit_return_unlock_condition_description,
        storage_deposit_return_unlock_condition_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(StorageDepositReturnUnlockCondition())


# Timelock Unlock Condition

timelock_unlock_condition_name = "Timelock Unlock Condition"
timelock_unlock_condition_description = (
    "Defines a slot index until which the output can not be unlocked."
)
timelock_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(2, timelock_unlock_condition_name),
    SimpleField(
        "Slot Index",
        UInt64(),
        "Slot index starting from which the output can be consumed.",
    ),
]


def TimelockUnlock(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        timelock_unlock_condition_name,
        timelock_unlock_condition_description,
        timelock_unlock_condition_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(TimelockUnlock())

# Expiration Unlock Condition

expiration_unlock_condition_name = "Expiration Unlock Condition"
expiration_unlock_condition_description = "Defines a slot index until which only <i>Address</i>, defined in <i>Address Unlock Condition</i>, is allowed to unlock the output. After the slot index is reached/passed, only <i>Return Address</i> can unlock it."
expiration_unlock_condition_return_address = ComplexField(
    "Return Address", OneOf(), regular_addresses_plus_multi_and_restricted
)

expiration_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(3, expiration_unlock_condition_name, article="an"),
    expiration_unlock_condition_return_address,
    SimpleField(
        "Slot Index",
        UInt64(),
        "Before this slot index, <i>Address Unlock Condition</i> is allowed to unlock the output, after that only the address defined in <i>Return Address</i>.",
    ),
]


def ExpirationUnlockCondition(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        expiration_unlock_condition_name,
        expiration_unlock_condition_description,
        expiration_unlock_condition_fields,
        tipReference=38,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ExpirationUnlockCondition())

# State Controller Address Unlock Condition

state_controller_unlock_condition_name = "State Controller Address Unlock Condition"
state_controller_unlock_condition_description = "Defines the State Controller Address that owns this output. It can unlock the output with the proper <i>Unlock</i> in a transaction that state transitions the account output."
state_controller_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(4, state_controller_unlock_condition_name),
    ComplexField("Address", OneOf(), regular_addresses_plus_multi_and_restricted),
]


def StateControllerUnlockCondition(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        state_controller_unlock_condition_name,
        state_controller_unlock_condition_description,
        state_controller_unlock_condition_fields,
        mandatory=True,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(StateControllerUnlockCondition())

# Governor Address Unlock Condition

governor_unlock_condition_name = "Governor Address Unlock Condition"
governor_unlock_condition_description = "Defines the Governor Address that owns this output. It can unlock the output with the proper <i>Unlock</i> in a transaction that governance transitions the account output."
governor_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(5, governor_unlock_condition_name),
    ComplexField("Address", OneOf(), regular_addresses_plus_multi_and_restricted),
]


def GovernorUnlockCondition(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        governor_unlock_condition_name,
        governor_unlock_condition_description,
        governor_unlock_condition_fields,
        mandatory=True,
        tipReference=42,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(GovernorUnlockCondition())

# Immutable Account Address Unlock Condition

immutable_account_address_unlock_condition_name = (
    "Immutable Account Address Unlock Condition"
)
immutable_account_address_unlock_condition_description = (
    "Defines the permanent <i>Account Address</i> that owns this output."
)
immutable_account_address_unlock_condition_fields: List[Field] = [
    unlock_condition_type_field(
        6, immutable_account_address_unlock_condition_name, article="an"
    ),
    ComplexField("Address", OneOf(), [AccountAddress()]),
]


def ImmutableAccountAddressUnlockCondition(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        immutable_account_address_unlock_condition_name,
        immutable_account_address_unlock_condition_description,
        immutable_account_address_unlock_condition_fields,
        mandatory=True,
        tipReference=44,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ImmutableAccountAddressUnlockCondition())
