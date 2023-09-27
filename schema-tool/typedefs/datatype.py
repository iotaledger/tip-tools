from dataclasses import dataclass
from abc import ABC, abstractmethod


class DataType(ABC):
    @abstractmethod
    def min_size(self) -> int:
        """Returns the minimum size the data type takes up in bytes."""
        pass

    @abstractmethod
    def max_size(self) -> int:
        """Returns the maximum size the data type takes up in bytes."""
        pass


class UInt8(DataType):
    def __str__(self) -> str:
        return "uint8"

    def min_size(self) -> int:
        return 1

    def max_size(self) -> int:
        return 1


class UInt16(DataType):
    def __str__(self) -> str:
        return "uint16"

    def min_size(self) -> int:
        return 2

    def max_size(self) -> int:
        return 2


class UInt32(DataType):
    def __str__(self) -> str:
        return "uint32"

    def min_size(self) -> int:
        return 4

    def max_size(self) -> int:
        return 4


class UInt64(DataType):
    def __str__(self) -> str:
        return "uint64"

    def min_size(self) -> int:
        return 8

    def max_size(self) -> int:
        return 8


class UInt256(DataType):
    def __str__(self) -> str:
        return "uint256"

    def min_size(self) -> int:
        return 32

    def max_size(self) -> int:
        return 32

@dataclass
class ByteArray(DataType):
    byteSize: int

    def __str__(self) -> str:
        return f"ByteArray[{self.byteSize}]"

    def min_size(self) -> int:
        return self.byteSize

    def max_size(self) -> int:
        return self.byteSize


@dataclass(init=False)
class LengthPrefixedArray(DataType):
    typePrefix: UInt8 | UInt16 | UInt32
    """The type of the length prefix"""
    typeElement: DataType
    """The type of the array elements"""
    minLength: int
    "The minimum size in bytes for the storage deposit calculation"
    maxLength: int
    "The maximum size in bytes for the storage deposit calculation"

    def __init__(
        self,
        typePrefix: UInt8 | UInt16 | UInt32,
        typeElement: DataType = UInt8(),
        minLength: int = 0,
        maxLength: int = 0,
    ) -> None:
        self.typePrefix = typePrefix
        self.typeElement = typeElement
        self.minLength = minLength
        self.maxLength = maxLength

    def __str__(self) -> str:
        match self.typeElement:
            case UInt8():
                # Stick with the convention of using "Byte" instead of "Uint8".
                typeName = "Byte"
            case _:
                typeName = str(self.typeElement).capitalize()

        return f"({self.typePrefix}){typeName}Array"

    def min_size(self) -> int:
        return self.typePrefix.min_size() + self.minLength

    def max_size(self) -> int:
        return self.typePrefix.max_size() + self.maxLength
