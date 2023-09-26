from typing import List, Tuple
from yattag.doc import Doc
from yattag.indentation import indent
from schemas.common import OutputOffset
from typedefs.datatype import (
    LengthPrefixedByteArray,
)
from typedefs.field import ComplexField, Schema, SimpleField
from typedefs.generation_type import GenerationType

from typedefs.subschema import AnyOf, AtMostOneOfEach, OneOf, OptAnyOf, OptOneOf

doc, tag, _ = Doc().tagtext()
# Generates unescaped text.
asis = doc.asis


def generateSchemaDeposit(schema: Schema, genType=GenerationType.Standalone) -> str:
    if genType == GenerationType.Standalone:
        with tag("details"):
            generateSummary(schema)
        generateSchema(schema, isTopLevel=True)
    elif genType == GenerationType.Embedded:
        with tag("details"):
            generateSummary(schema)
            generateSchema(schema)

    return indent(doc.getvalue())


def generateSummary(schema: Schema):
    with tag("summary"):
        asis(schema.name)
    if schema.summary is not None:
        with tag("blockquote"):
            asis(schema.summary)


def generateSchema(schema: Schema, isTopLevel=False):
    with tag("table"):
        if isTopLevel:
            generateSection("Offset", OutputOffset)
        generateSection("Fields", schema)
        if isTopLevel:
            generateVByteMinMax(schema)


def generateSection(section: str, schema: Schema):
    with tag("tr"):
        with tag("td"):
            asis(section)
        with tag("td"):
            with tag("table"):
                generateTableHeader()
                for field in schema.fields:
                    match field:
                        case SimpleField():
                            generateSimpleField(field)
                        case ComplexField():
                            generateComplexField(field)


def generateTableHeader():
    with tag("tr"):
        with tag("td"):
            asis("<b>Field</b>")
        with tag("td"):
            asis("<b>Field type</b>")
        with tag("td"):
            asis("<b>Length Minimum</b>")
        with tag("td"):
            asis("<b>Length Maximum</b>")


def generateSimpleField(field: SimpleField):
    # Handle the length prefixed byte array specially during rendering.
    # Add an extra field for the length prefix and subtract that from the field itself.
    lengthPrefixMin = 0
    lengthPrefixMax = 0
    if isinstance(field.type, LengthPrefixedByteArray):
        generateSimpleField(
            SimpleField(
                field.name + " Length",
                field.type.typePrefix,
                "Length of the following field.",
            )
        )
        lengthPrefixMin = field.type.typePrefix.min_size()
        lengthPrefixMax = field.type.typePrefix.max_size()

    with tag("tr"):
        with tag("td"):
            asis(field.name)
        with tag("td"):
            asis(str(field.deposit_weight))
        with tag("td"):
            asis(str(field.type.min_size() - lengthPrefixMin))
        with tag("td"):
            asis(str(field.type.max_size() - lengthPrefixMax))


def generateComplexField(field: ComplexField):
    with tag("tr"):
        with tag("td", ("valign", "top")):
            asis(field.name + " " + str(field.subschema))
        with tag("td", ("colspan", 2)):
            for schema in field.schemas:
                generateSchemaDeposit(schema, genType=GenerationType.Embedded)


def generateVByteMinMax(schema: Schema):
    offsetMinSize, offsetMaxSize = calculateDeposit(OutputOffset, debug=False)
    minSize, maxSize = calculateDeposit(schema, debug=False)

    minSize += offsetMinSize
    maxSize += offsetMaxSize

    with tag("tr"):
        with tag("td"):
            asis("v_byte Minimum")
        with tag("td"):
            asis(str(minSize))
    with tag("tr"):
        with tag("td"):
            asis("v_byte Maximum")
        with tag("td"):
            asis(str(maxSize))


def calculateDeposit(schema: Schema, debug=False) -> Tuple[int, int]:
    minSize = 0
    maxSize = 0

    for field in schema.fields:
        match field:
            case SimpleField():
                min, max = fieldSize(field)
                minSize += min
                maxSize += max
                if debug:
                    print(f"Added {field.name} with minLength={min}, maxLength={max}")
            case ComplexField():
                match field.subschema:
                    case OptAnyOf():
                        # minSize unaffected, since its optional
                        min, max = anyOfSchemaDeposit(field.subschema, field.schemas)
                        maxSize += max
                        if debug:
                            print(
                                f"Added {field.name} with minLength={min}, maxLength={max}"
                            )
                    case OptOneOf():
                        # minSize unaffected, since its optional
                        min, max = oneOfSchemaDeposit(field.schemas)
                        maxSize += max
                        if debug:
                            print(
                                f"Added {field.name} with minLength={min}, maxLength={max}"
                            )
                    case OneOf():
                        min, max = oneOfSchemaDeposit(field.schemas)
                        minSize += min
                        maxSize += max
                        if debug:
                            print(
                                f"Added {field.name} with minLength={min}, maxLength={max}"
                            )
                    case AtMostOneOfEach():
                        min, max = atMostOneOfEachSchemaDeposit(field.schemas)
                        minSize += min
                        maxSize += max
                        if debug:
                            print(
                                f"Added {field.name} with minLength={min}, maxLength={max}"
                            )
                    case AnyOf():
                        min, max = anyOfSchemaDeposit(field.subschema, field.schemas)
                        minSize += min
                        maxSize += max
                        if debug:
                            print(
                                f"Added {field.name} with minLength={min}, maxLength={max}"
                            )

    if debug:
        print(f"{schema.name} has {minSize}, {maxSize}")

    return minSize, maxSize


def fieldSize(field: SimpleField) -> Tuple[int, int]:
    weight = field.deposit_weight.weight()

    minSize = field.type.min_size()
    maxSize = field.type.max_size()

    return weight * minSize, weight * maxSize


def atMostOneOfEachSchemaDeposit(schemas: List[Schema]) -> Tuple[int, int]:
    """Calculates the minimum and maximum size for an atMostOneOfEach Subschema."""
    # Only include schemas that are mandatory.
    minimallySizedSchemas = [
        calculateDeposit(schema)[0] for schema in schemas if schema.mandatory
    ]
    # Include all schemas.
    maximallySizedSchemas = [calculateDeposit(schema)[1] for schema in schemas]

    # The sum of deposits of all minimally-sized (mandatory) schemas.
    minSize = sum(minimallySizedSchemas)

    # The sum of deposits of all maximally-sized schemas.
    maxSize = sum(maximallySizedSchemas)

    return minSize, maxSize


def oneOfSchemaDeposit(schemas: List[Schema]) -> Tuple[int, int]:
    """Calculates the minimum and maximum size for a oneOf Subschema."""
    minimallySizedSchemas = [calculateDeposit(schema)[0] for schema in schemas]
    maximallySizedSchemas = [calculateDeposit(schema)[1] for schema in schemas]

    # The minimum of all the minimally-sized schemas.
    minSize = min(minimallySizedSchemas)

    # The maximum of all the maximally-sized schemas.
    maxSize = max(maximallySizedSchemas)

    return minSize, maxSize


def anyOfSchemaDeposit(
    subschema: AnyOf | OptAnyOf, schemas: List[Schema]
) -> Tuple[int, int]:
    """Calculates the minimum and maximum size for an anyOf Subschema."""

    minSize, maxSize = oneOfSchemaDeposit(schemas)

    minSize *= subschema.minLength
    maxSize *= subschema.maxLength

    return minSize, maxSize
