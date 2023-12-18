from enum import Enum
from typing import Dict, Optional


class DepositWeight(Enum):
    Data = 1
    Key = 2
    BlockIssuerKey = 3
    Staking = 4
    Delegation = 5

    def __str__(self) -> str:
        match self:
            case DepositWeight.Data:
                return "<code>data</code>"
            case DepositWeight.Key:
                return "<code>key</code>"
            case DepositWeight.BlockIssuerKey:
                return "<code>block_issuer_key</code>"
            case DepositWeight.Staking:
                return "<code>staking</code>"
            case DepositWeight.Delegation:
                return "<code>delegation</code>"


class RentStructure:
    rent_structure: Dict[DepositWeight, int]

    def __init__(
        self,
        block_issuer_key: Optional[int] = None,
        staking: Optional[int] = None,
        delegation: Optional[int] = None,
    ):
        self.rent_structure = {
            DepositWeight.Data: 1,
            DepositWeight.Key: 10,
            DepositWeight.BlockIssuerKey: 100
            if block_issuer_key is None
            else block_issuer_key,
            DepositWeight.Staking: 100 if staking is None else staking,
            DepositWeight.Delegation: 100 if delegation is None else delegation,
        }

    def weight(self, deposit_weight: DepositWeight) -> int:
        return self.rent_structure[deposit_weight]