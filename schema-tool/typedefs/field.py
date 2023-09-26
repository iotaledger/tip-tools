from dataclasses import dataclass
from typing import List, Optional
from typedefs.datatype import DataType
from typedefs.deposit_weight import DepositWeight
from typedefs.subschema import Subschema

ALL_SCHEMAS = []


class Field:
    pass


@dataclass(init=False)
class Schema:
    name: str
    summary: Optional[str]
    fields: List[Field]
    mandatory: bool
    """Whether this schema is mandatory to be present when it is embedded."""

    def __init__(
        self,
        name: str,
        summary: Optional[str],
        fields: List[Field],
        mandatory: bool = False,
    ):
        self.name = name
        self.summary = summary
        self.fields = fields
        self.mandatory = mandatory

        ALL_SCHEMAS.append(self)


@dataclass(init=False)
class SimpleField(Field):
    name: str
    type: DataType
    deposit_weight: DepositWeight
    description: str

    def __init__(
        self,
        name: str,
        type: DataType,
        description: str,
        deposit_weight: DepositWeight = DepositWeight.Data,
    ):
        self.name = name
        self.type = type
        self.description = description
        self.deposit_weight = deposit_weight


@dataclass(init=False)
class ComplexField(Field):
    name: str
    subschema: Subschema
    schemas: List[Schema]

    def __init__(
        self,
        name: str,
        subschema: Subschema,
        schemas: List[Schema],
    ):
        self.name = name
        self.subschema = subschema
        self.schemas = schemas
