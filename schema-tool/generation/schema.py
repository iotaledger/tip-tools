from yattag.doc import Doc
from yattag.indentation import indent
from typedefs.field import ComplexField, Schema, SimpleField
from typedefs.generation_type import GenerationType
from typedefs.subschema import Embedded

doc, tag, _ = Doc().tagtext()
# Generates unescaped text.
asis = doc.asis


def generateSchemaWithSummary(schema: Schema, genType: GenerationType) -> str:
    if genType == GenerationType.Standalone:
        if schema.summary is not None:
            with tag("details"):
                generateSummary(schema, genType)
        generateSchema(schema)

    elif genType == GenerationType.Embedded:
        with tag("details"):
            if schema.detailsOpen:
                doc.attr(open="true")
            generateSummary(schema, genType)
            if not schema.omitFields:
                generateSchema(schema)

    return indent(doc.getvalue())


def generateSummary(schema: Schema, genType: GenerationType):
    with tag("summary"):
        asis(schema.name)
    if schema.summary is not None:
        with tag("blockquote"):
            if schema.tipRef is not None and genType == GenerationType.Embedded:
                summary = schema.summary + " " + schema.definedIn()
            else:
                summary = schema.summary

            asis(summary)


def generateSchema(schema: Schema):
    with tag("table"):
        with tag("tr"):
            with tag("td"):
                asis("<b>Name</b>")
            with tag("td"):
                asis("<b>Type</b>")
            with tag("td"):
                asis("<b>Description</b>")
        for field in schema.fields:
            match field:
                case SimpleField():
                    generateSimpleField(field)
                case ComplexField():
                    generateComplexField(field)


def generateSimpleField(field: SimpleField):
    with tag("tr"):
        with tag("td"):
            asis(field.name)
        with tag("td"):
            asis(str(field.type))
        with tag("td"):
            asis(field.description)


def generateComplexField(field: ComplexField):
    with tag("tr"):
        with tag("td", ("valign", "top")):
            fieldName = field.name
            match field.subschema:
                case Embedded():
                    pass
                case _:
                    fieldName = fieldName + " <code>" + str(field.subschema) + "</code>"
            asis(fieldName)
        with tag("td", ("colspan", 2)):
            for schema in field.schemas:
                generateSchemaWithSummary(schema, GenerationType.Embedded)
