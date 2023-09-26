from typing import List
from typedefs.datatype import (
    ByteArray,
    UInt256,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.subschema import OptAnyOf

MAX_NATIVE_TOKEN_COUNT = 64

native_token_id = SimpleField(
    "Token ID", ByteArray(38), "Identifier of the native token. Its derivation is defined in <a href='../TIP-0044/tip-0044.md#foundry-output'>TIP-44</a>."
)
native_token_amount = SimpleField(
    "Amount", UInt256(), "Amount of native tokens of the given <i>Token ID</i>."
)
native_token_fields: List[Field] = [native_token_id, native_token_amount]
native_token = Schema("Native Token", None, native_token_fields)

NativeTokensCountField = SimpleField(
    "Native Tokens Count", UInt8(), "The number of different native tokens held by the output."
)

NativeTokens = ComplexField(
    "Native Tokens",
    OptAnyOf(MAX_NATIVE_TOKEN_COUNT),
    [native_token],
)
