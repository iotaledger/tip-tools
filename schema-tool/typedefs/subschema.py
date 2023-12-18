from abc import ABC
from dataclasses import dataclass


class Subschema(ABC):
    """https://github.com/iotaledger/tips/blob/main/tips/TIP-0021/tip-0021.md#subschemas"""

    pass

class Embedded(Subschema):
    """The subschema where the schema is unconditionally embedded."""
    pass

    def __str__(self) -> str:
        raise TypeError("Embedded cannot be stringified")

class OneOf(Subschema):
    pass

    def __str__(self) -> str:
        return "oneOf"


class OptOneOf(Subschema):
    pass

    def __str__(self) -> str:
        return "optOneOf"


@dataclass
class AnyOf(Subschema):
    minLength: int
    maxLength: int

    def __str__(self) -> str:
        return "anyOf"


@dataclass
class OptAnyOf(Subschema):
    maxLength: int
    minLength: int = 0

    def __str__(self) -> str:
        return "optAnyOf"


class AtMostOneOfEach(Subschema):
    pass

    def __str__(self) -> str:
        return "atMostOneOfEach"
