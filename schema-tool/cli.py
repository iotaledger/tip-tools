import argparse
from enum import Enum


# Star import needed for all the structures to be initialized.
from schemas import *
from generation.deposit import generateSchemaDeposit
from generation.schema import GenerationType, generateSchemaWithSummary
from generation.deposit_test import RunDepositCalculationTests


class Commands(Enum):
    SCHEMA = "schema"
    DEPOSIT = "deposit"
    TEST = "test"


def main():
    parser = argparse.ArgumentParser(description="Schema Tool CLI")

    subparsers = parser.add_subparsers(
        title="Subcommands", dest="operation", required=True
    )

    schema_parser = subparsers.add_parser(
        Commands.SCHEMA.value, help="Generate type schema."
    )
    schema_parser.add_argument(
        "schema_name",
        type=str,
        help="The name of the schema to generate.",
    )
    generationTypes = [variant.value for variant in GenerationType]
    schema_parser.add_argument(
        "--type",
        "-t",
        type=GenerationType,
        default=GenerationType.Standalone,
        help=f"The type of table structure to generate the schema in. Possible values: {generationTypes}.",
        required=False,
    )
    schema_parser.add_argument(
        "--dry-run",
        "-d",
        type=bool,
        default=False,
        help=f"Does not print the result when set to true.",
        required=False,
    )

    deposit_parser = subparsers.add_parser(
        Commands.DEPOSIT.value, help="Generate deposit schema."
    )
    deposit_parser.add_argument(
        "schema_name",
        type=str,
        help="The name of the schema to generate.",
    )
    deposit_parser.add_argument(
        "--dry-run",
        "-d",
        type=bool,
        default=False,
        help=f"Does not print the result when set to true.",
        required=False,
    )

    subparsers.add_parser(Commands.TEST.value, help="Run tests.")

    args = parser.parse_args()
    operation = args.operation
    args = vars(args)

    match operation:
        case Commands.SCHEMA.value:
            generateSchema(args["schema_name"], args["type"], dry_run=args["dry_run"])
        case Commands.DEPOSIT.value:
            generateDeposit(args["schema_name"], dry_run=args["dry_run"])
        case Commands.TEST.value:
            RunDepositCalculationTests()
        case _:
            parser.print_help()


def get_schema(schema_name: str) -> Schema | None:
    def find_schema(structure_name):
        for struct in AVAILABLE_SCHEMAS:
            if struct.name == structure_name:
                return struct
        return None

    schema = find_schema(schema_name)
    if schema is None:
        print(f"No schema with name `{schema_name}` exists.")
        print("Available schemas:")
        for schema in AVAILABLE_SCHEMAS:
            print(f'"{schema.name}"')
        return None
    else:
        return schema


def generateSchema(
    schema_name: str, generationType: GenerationType, dry_run: bool = False
):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaWithSummary(schema, generationType)
        if not dry_run:
            print(generated)


def generateDeposit(schema_name: str, dry_run: bool = False):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaDeposit(schema)
        if not dry_run:
            print(generated)


if __name__ == "__main__":
    main()
