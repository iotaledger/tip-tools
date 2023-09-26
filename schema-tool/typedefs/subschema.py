from abc import ABC
from dataclasses import dataclass


class Subschema(ABC):
    """https://github.com/iotaledger/tips/blob/main/tips/TIP-0021/tip-0021.md#subschemas"""

    pass


class OneOf(Subschema):
    pass

    def __str__(self) -> str:
        return "<code>oneOf</code>"


class OptOneOf(Subschema):
    pass

    def __str__(self) -> str:
        return "<code>optOneOf</code>"


@dataclass
class AnyOf(Subschema):
    minLength: int
    maxLength: int

    def __str__(self) -> str:
        return "<code>anyOf</code>"


@dataclass
class OptAnyOf(Subschema):
    maxLength: int
    minLength: int = 0

    def __str__(self) -> str:
        return "<code>optAnyOf</code>"


class AtMostOneOfEach(Subschema):
    pass

    def __str__(self) -> str:
        return "<code>atMostOneOfEach</code>"
