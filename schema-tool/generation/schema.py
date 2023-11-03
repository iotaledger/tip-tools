from typing import Any
from yattag import SimpleDoc
from yattag.doc import Doc
from yattag.indentation import indent
from typedefs.field import ComplexField, Schema, SimpleField
from typedefs.generation_type import GenerationType
from typedefs.subschema import Embedded


class SchemaGen:
    doc: SimpleDoc
    tag: Any
    asis: Any

    def __init__(self) -> None:
        self.doc = Doc()
        _, self.tag, _ = self.doc.tagtext()
        self.asis = self.doc.asis

    def generateSchemaWithSummary(self, schema: Schema, genType: GenerationType) -> str:
        if genType == GenerationType.Standalone:
            if schema.summary is not None:
                with self.tag("details"):
                    self.generateSummary(schema, genType)
            self.generateSchema(schema)

        elif genType == GenerationType.Embedded:
            with self.tag("details"):
                if schema.detailsOpen:
                    self.doc.attr(open="true")
                self.generateSummary(schema, genType)
                if not schema.omitFields:
                    self.generateSchema(schema)

        return indent(self.doc.getvalue())

    def generateSummary(self, schema: Schema, genType: GenerationType):
        with self.tag("summary"):
            self.asis(schema.name)
        if schema.summary is not None:
            with self.tag("blockquote"):
                if schema.tipRef is not None and genType == GenerationType.Embedded:
                    summary = schema.summary + " " + schema.definedIn()
                else:
                    summary = schema.summary

                self.asis(summary)

    def generateSchema(self, schema: Schema):
        with self.tag("table"):
            with self.tag("tr"):
                with self.tag("td"):
                    self.asis("<b>Name</b>")
                with self.tag("td"):
                    self.asis("<b>Type</b>")
                with self.tag("td"):
                    self.asis("<b>Description</b>")
            for field in schema.fields:
                match field:
                    case SimpleField():
                        self.generateSimpleField(field)
                    case ComplexField():
                        self.generateComplexField(field)

    def generateSimpleField(self, field: SimpleField):
        with self.tag("tr"):
            with self.tag("td"):
                self.asis(field.name)
            with self.tag("td"):
                self.asis(str(field.type))
            with self.tag("td"):
                self.asis(field.description)

    def generateComplexField(self, field: ComplexField):
        with self.tag("tr"):
            with self.tag("td", ("valign", "top")):
                fieldName = field.name
                match field.subschema:
                    case Embedded():
                        pass
                    case _:
                        fieldName = (
                            fieldName + " <code>" + str(field.subschema) + "</code>"
                        )
                self.asis(fieldName)
            with self.tag("td", ("colspan", 2)):
                for schema in field.schemas:
                    self.generateSchemaWithSummary(schema, GenerationType.Embedded)
