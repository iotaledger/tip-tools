from enum import Enum


class DepositWeight(Enum):
    Data = 1
    Key = 2
    BlockIssuerKey = 3
    Staking = 4
    Delegation = 5

    def weight(self) -> int:
        match self:
            case DepositWeight.Data:
                return 1
            case DepositWeight.Key:
                return 10
            # TODO: Set correct value.
            case DepositWeight.BlockIssuerKey:
                return 100
            # TODO: Set correct value.
            case DepositWeight.Staking:
                return 100
            # TODO: Set correct value.
            case DepositWeight.Delegation:
                return 100

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
