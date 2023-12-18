from typing import List
from schemas.candidacy_announcement import CandidacyAnnouncement
from schemas.common import AVAILABLE_SCHEMAS
from schemas.signature import Ed25519Signature
from schemas.tagged_data import TaggedData
from schemas.transaction import SignedTransaction
from typedefs.datatype import (
    ByteArray,
    LengthPrefixedArray,
    UInt32,
    UInt64,
    UInt8,
)
from typedefs.field import ComplexField, Field, Schema, SimpleField, TipReference
from typedefs.subschema import AnyOf, Embedded, OneOf, OptAnyOf, OptOneOf


def block_body_type(type_value: int, name: str, article="a") -> SimpleField:
    return SimpleField(
        "Block Body Type",
        UInt8(),
        f"Set to <strong>value {type_value}</strong> to denote {article} <i>{name}</i>.",
    )


def BlockHeader(
    omitFields: bool = False,
    detailsOpen: bool = False,
) -> Schema:
    return Schema(
        "Block Header",
        "The common header fields of a block.",
        [
            SimpleField(
                "Protocol Version",
                UInt8(),
                "This field denotes what protocol rules apply to the block.",
            ),
            SimpleField(
                "Network ID",
                UInt64(),
                "Network identifier. Usually, it will be set to the first 8 bytes of the BLAKE2b-256 hash of the concatenation of the network type and the protocol version string.",
            ),
            SimpleField(
                "Issuing Time",
                UInt64(),
                "The time at which the block was issued. It is a Unix timestamp in nanoseconds.",
            ),
            SimpleField(
                "Slot Commitment ID",
                ByteArray(36),
                "The identifier of the slot this block commits to. More details in the <a href='#slot-commitment-id'>Slot Commitment ID section</a>.",
            ),
            SimpleField(
                "Latest Finalized Slot",
                UInt32(),
                "The slot index of the latest finalized slot.",
            ),
            SimpleField(
                "Issuer ID",
                ByteArray(32),
                "The identifier of the account that issued this block.",
            ),
        ],
        omitFields=omitFields,
        detailsOpen=detailsOpen,
    )


def Parent(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        "Parent",
        "A reference to a block.",
        [
            SimpleField("Block ID", ByteArray(36), "The Block ID of the parent."),
        ],
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Parent())

basic_block_body_name = "Basic Block Body"


def BasicBlockBody(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        basic_block_body_name,
        "The basic block body.",
        [
            block_body_type(0, basic_block_body_name),
            SimpleField(
                "Strong Parents Count",
                UInt8(),
                "The number of blocks following, which are strongly directly approved.",
            ),
            ComplexField(
                "Strong Parents",
                AnyOf(minLength=1, maxLength=8),
                [Parent()],
            ),
            SimpleField(
                "Weak Parents Count",
                UInt8(),
                "The number of blocks following, which are weakly directly approved.",
            ),
            ComplexField("Weak Parents", OptAnyOf(maxLength=8), [Parent()]),
            SimpleField(
                "Shallow Like Parents Count",
                UInt8(),
                "The number of blocks following, which are directly referenced to adjust opinion.",
            ),
            ComplexField("Shallow Like Parents", OptAnyOf(maxLength=8), [Parent()]),
            SimpleField(
                "Payload Length",
                UInt32(),
                "The length of the following payload in bytes. A length of 0 means no payload will be attached.",
            ),
            ComplexField(
                "Payload",
                OptOneOf(),
                [
                    SignedTransaction(omitFields=True),
                    TaggedData(omitFields=True),
                    CandidacyAnnouncement(omitFields=True),
                ],
            ),
            SimpleField(
                "Max Burned Mana",
                UInt64(),
                "The amount of Mana the Account identified by <code>Issuer ID</code> is at most willing to burn for this block. The actual Mana deducted from this Account's Block Issuance Credit may be lower than the value of this field which is the product of the block's work score and the RMC (Reference Mana Cost) from the block's slot commitment, identified by the <code>Slot Commitment ID</code>. Therefore, for the calculation of this field, the block issuer should also use the RMC value from the same commitment.",
            ),
        ],
        tipReference=TipReference(46, "basic-block"),
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(BasicBlockBody())


validation_block_body_name = "Validation Block Body"


def ValidationBlockBody(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        validation_block_body_name,
        "The validation block body.",
        [
            block_body_type(1, validation_block_body_name),
            SimpleField(
                "Strong Parents Count",
                UInt8(),
                "The number of blocks following, which are strongly directly approved.",
            ),
            ComplexField(
                "Strong Parents",
                AnyOf(minLength=1, maxLength=50),
                [Parent()],
            ),
            SimpleField(
                "Weak Parents Count",
                UInt8(),
                "The number of blocks following, which are weakly directly approved.",
            ),
            ComplexField("Weak Parents", OptAnyOf(maxLength=50), [Parent()]),
            SimpleField(
                "Shallow Like Parents Count",
                UInt8(),
                "The number of blocks following, which are directly referenced to adjust opinion.",
            ),
            ComplexField("Shallow Like Parents", OptAnyOf(maxLength=50), [Parent()]),
            SimpleField(
                "Highest Supported Version",
                UInt8(),
                "The highest supported protocol version the issuer of this block supports.",
            ),
            SimpleField(
                "Protocol Parameters Hash",
                ByteArray(32),
                "The hash of the protocol parameters for the Highest Supported Version.",
            ),
        ],
        tipReference=TipReference(46, "validation-block"),
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(ValidationBlockBody())


def Block(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        "Block",
        "The block consisting of a header, body and signature.",
        [
            ComplexField("Header", Embedded(), [BlockHeader(detailsOpen=True)]),
            ComplexField(
                "Body",
                OneOf(),
                [BasicBlockBody(omitFields=True), ValidationBlockBody(omitFields=True)],
            ),
            ComplexField("Signature", OneOf(), [Ed25519Signature(omitFields=True)]),
        ],
        tipReference=46,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(Block())
