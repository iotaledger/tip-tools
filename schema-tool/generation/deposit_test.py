from dataclasses import dataclass
from generation.deposit import calculateOutputDeposit
from schemas.output_basic import BasicOutput
from schemas.output_foundry import FoundryOutput
from schemas.output_nft import NftOutput
from typedefs.deposit_weight import RentStructure
from typedefs.field import Schema


def RunDepositCalculationTests():
    @dataclass
    class Test:
        output: Schema
        expected_min_size: int
        expected_max_size: int

    # Numbers verified manually.
    # TODO: Add remaining output types.
    tests = [
        Test(BasicOutput, 450, 13509),
        Test(NftOutput, 483, 21771),
        Test(FoundryOutput, 544, 21414),
    ]

    for test in tests:
        print("Testing deposit calculation for", test.output.name)
        size = calculateOutputDeposit(test.output, RentStructure())
        assert size[0] == test.expected_min_size, f"expected: {test.expected_min_size}, actual: {size[0]}"
        # TODO: Reenable test after manually calculating new max values with new address types.
        # assert size[1] == test.expected_max_size, f"expected: {test.expected_max_size}, actual: {size[1]}"
