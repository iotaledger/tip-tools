#!/usr/bin/python3

import argparse
from enum import Enum
import os
import re
from typing import Optional, Tuple


# Star import needed for all the structures to be initialized.
from schemas import *
from generation.deposit import generateSchemaDeposit
from generation.schema import GenerationType, generateSchemaWithSummary
from generation.deposit_test import RunDepositCalculationTests


class Commands(Enum):
    SCHEMA = "schema"
    DEPOSIT = "deposit"
    TEST = "test"


class SchemaCommands(Enum):
    GENERATE = "generate"
    REPLACE = "replace"
    UPDATE = "update"


schema_name_argument = "schema_name"
schema_name_help = "The name of the schema to generate."
dry_run_argument = "dry_run"
dry_run_help = "Does not print the result when set to true."
tips_repo_path_argument = "tips_repo_path"
tips_repo_path_help = "The path to the tips repo."
tip_number_argument = "tip_number"
tip_number_help = "The number of the to-be-updated TIP."


def add_schema_parser(subparsers: argparse._SubParsersAction):
    schema_parser = subparsers.add_parser(
        Commands.SCHEMA.value, help="Schema operations."
    )

    schema_subparsers = schema_parser.add_subparsers(
        title="Schema Commands", dest="schema_operation", required=True
    )

    generate_parser = schema_subparsers.add_parser(
        SchemaCommands.GENERATE.value, help="Generate type schema to stdout."
    )
    replace_parser = schema_subparsers.add_parser(
        SchemaCommands.REPLACE.value,
        help="Replace type schema in TIP. Replaces the existing schema table in the TIP with the newly created one. The path to the tips repo must be given. The given schema will be replaced in the TIP in which it is defined. It must be defined at the top-level as a standalone schema. If the schema is embedded in other schemas, it will not be touched.",
    )
    update_parser = schema_subparsers.add_parser(
        SchemaCommands.UPDATE.value,
        help="Replaces all the existing schema tables in the TIP with the newly created ones. The path to TIP repo and the TIP number must be given. All the schemas defined in that TIP will be updated.",
    )

    generate_parser.add_argument(
        schema_name_argument,
        type=str,
        help=schema_name_help,
    )
    generate_parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        default=False,
        help=dry_run_help,
        required=False,
    )

    replace_parser.add_argument(
        tips_repo_path_argument,
        type=str,
        help=tips_repo_path_help,
    )
    replace_parser.add_argument(
        schema_name_argument,
        type=str,
        help=schema_name_help,
    )

    update_parser.add_argument(
        tips_repo_path_argument,
        type=str,
        help=tips_repo_path_help,
    )
    update_parser.add_argument(
        tip_number_argument,
        type=str,
        help=tip_number_help,
    )


def main():
    parser = argparse.ArgumentParser(description="Schema Tool CLI")

    subparsers = parser.add_subparsers(
        title="Subcommands", dest="operation", required=True
    )

    add_schema_parser(subparsers)

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
        action="store_true",
        default=False,
        help=dry_run_help,
        required=False,
    )

    subparsers.add_parser(Commands.TEST.value, help="Run tests.")

    args = parser.parse_args()
    operation = args.operation
    schema_operation = args.schema_operation
    args = vars(args)

    match operation:
        case Commands.SCHEMA.value:
            match schema_operation:
                case SchemaCommands.GENERATE.value:
                    generateSchemaCommand(
                        args[schema_name_argument],
                        GenerationType.Standalone,
                        dry_run=args[dry_run_argument],
                    )
                case SchemaCommands.REPLACE.value:
                    replaceSchemaCommand(
                        args[schema_name_argument], args[tips_repo_path_argument]
                    )
                case SchemaCommands.UPDATE.value:
                    updateSchemaCommand(
                        args[tips_repo_path_argument], args[tip_number_argument]
                    )
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


def generateSchemaCommand(
    schema_name: str,
    generationType: GenerationType,
    dry_run: bool = False,
):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaWithSummary(schema, generationType)
        if not dry_run:
            print(generated)


def replaceSchemaCommand(
    schema_name: str,
    tips_repo_path: str,
):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaWithSummary(schema, GenerationType.Standalone)
        if schema.tipRef is not None:
            replaceSchema(
                tips_repo_path, schema.name, schema.tipRef.tipNumber, generated
            )
        else:
            print("Tip number on schema must be set for replacing.")


def updateSchemaCommand(
    tips_repo_path: str,
    tip_number_str: str,
):
    tip_number: int = int(tip_number_str)

    for schema in AVAILABLE_SCHEMAS:
        if schema.tipRef is not None and schema.tipRef.tipNumber == tip_number:
            generated: str = generateSchemaWithSummary(
                schema, GenerationType.Standalone
            )
            replaceSchema(tips_repo_path, schema.name, tip_number, generated)


def generateDeposit(schema_name: str, dry_run: bool = False):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaDeposit(schema)
        if not dry_run:
            print(generated)


def replaceSchema(tipRepoPath: str, name: str, tip: int, generated: str):
    paddedTipNo = f"{tip:04}"
    tipPath = os.path.join(tipRepoPath, f"tips/TIP-{paddedTipNo}/tip-{paddedTipNo}.md")

    if not os.path.exists(tipPath):
        print(
            f'This schema is defined in TIP-{paddedTipNo}, but path "{tipPath}" does not exist.'
        )
        return

    with open(tipPath, "r") as f:
        tip_content = f.read()

    # Match the entire HTML section in which the schema is defined: <details>...</table>.
    pattern = rf"^<details>\s*<summary>{name}<\/summary>.*?^<\/table>"

    # - DOTALL so that . also match newlines
    # - MULTILINE so that ^ matches not just the start of the string but also the start of a line.
    mat = re.search(pattern, tip_content, flags=re.DOTALL | re.MULTILINE)

    if mat is None:
        print(f'Did not find schema "{name}" at the top-level in TIP-{paddedTipNo}.')
        return

    (start, end) = mat.span()
    print(f'Replaced schema "{name}" in TIP-{paddedTipNo}.')

    part1 = tip_content[:start]
    part2 = generated
    part3 = tip_content[end:]

    with open(tipPath, "w") as f:
        f.write(part1 + part2 + part3)


if __name__ == "__main__":
    main()
