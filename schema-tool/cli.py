#!/usr/bin/python3

import argparse
from enum import Enum
import os
import re
from typing import Optional


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
    schema_parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        default=False,
        help=f"Does not print the result when set to true.",
        required=False,
    )
    schema_parser.add_argument(
        "--replace",
        "-r",
        type=str,
        metavar="PATH_TO_TIPS_REPO",
        help=f"Replaces the existing table in the TIP with the newly created one. The path to the tips repo must be given. The given schema will be replaced in the TIP in which it is defined. It must be defined at the top-level as a standalone schema. If the schema is embedded in other schemas, it will not be touched.",
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
        action="store_true",
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
            generateSchema(
                args["schema_name"],
                GenerationType.Standalone,
                dry_run=args["dry_run"],
                replace=args["replace"],
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


def generateSchema(
    schema_name: str,
    generationType: GenerationType,
    dry_run: bool = False,
    replace: Optional[str] = None,
):
    schema = get_schema(schema_name)
    if schema is None:
        return
    else:
        generated: str = generateSchemaWithSummary(schema, generationType)
        if not dry_run and not replace:
            print(generated)
        elif replace:
            if schema.tipRef is not None:
                replaceSchema(replace, schema.name, schema.tipRef.tipNumber, generated)
            else:
                print("Tip number on schema must be set for replacing.")


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
        print(f'This schema is defined in TIP-{paddedTipNo}, but path "{tipPath}" does not exist.')
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
