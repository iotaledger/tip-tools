from dataclasses import dataclass
from typing import List, Optional
from typedefs.datatype import DataType
from typedefs.deposit_weight import DepositWeight
from typedefs.subschema import Subschema

ALL_SCHEMAS = []


class Field:
    pass


@dataclass(init=False)
class TipReference:
    tipNumber: int
    """The TIP number in which this schema is defined."""
    customFragment: Optional[str]
    """A custom link (fragment = '#') within the TIP to which the reference should point."""

    def __init__(
        self,
        tipNumber: int,
        customFragment: Optional[str] = None,
    ) -> None:
        self.tipNumber = tipNumber
        self.customFragment = customFragment


@dataclass(init=False)
class Schema:
    name: str
    summary: str
    fields: List[Field]
    mandatory: bool
    """Whether this schema is mandatory to be present when it is embedded."""
    omitFields: bool
    """Whether to omit the fields and only render the description."""
    detailsOpen: bool
    """Whether the details of the schema are visible by default or not."""
    tipRef: Optional[TipReference]
    """The TIP number in which this schema is defined."""

    def __init__(
        self,
        name: str,
        summary: str,
        fields: List[Field],
        mandatory: bool = False,
        omitFields: bool = False,
        detailsOpen: bool = False,
        tipReference: Optional[int | TipReference] = None,
    ):
        self.name = name
        self.summary = summary
        self.fields = fields
        self.mandatory = mandatory
        self.omitFields = omitFields
        self.detailsOpen = detailsOpen

        match tipReference:
            case int():
                self.tipRef = TipReference(tipReference)
            case _:
                self.tipRef = tipReference

        ALL_SCHEMAS.append(self)

    def definedIn(self) -> str:
        definedIn = ""
        if self.tipRef is not None:
            if self.tipRef.customFragment is None:
                # Generate the fragment from the name.
                fragment = "-".join([part.lower() for part in self.name.split(" ")])
                linkName = self.name
            else:
                fragment = self.tipRef.customFragment
                linkName = " ".join([part.capitalize() for part in fragment.split("-")])

            paddedTipNo = f"{self.tipRef.tipNumber:04}"
            definedIn = f"Defined in <a href='../TIP-{paddedTipNo}/tip-{paddedTipNo}.md#{fragment}'>TIP-{self.tipRef.tipNumber} ({linkName})</a>."
        return definedIn


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
