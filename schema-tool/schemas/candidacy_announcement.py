from typing import List

from schemas.common import AVAILABLE_SCHEMAS, payload_type_field
from typedefs.field import Field, Schema

candidacy_announcement_name = "Candidacy Announcement"
candidacy_announcement_fields: List[Field] = [
    payload_type_field(2, f"{candidacy_announcement_name} Payload"),
]


def CandidacyAnnouncement(
    omitFields: bool = False,
) -> Schema:
    return Schema(
        candidacy_announcement_name,
        "Signals candidacy for committee selection for the epoch after the one in which it is issued.",
        candidacy_announcement_fields,
        tipReference=40,
        omitFields=omitFields,
    )


AVAILABLE_SCHEMAS.append(CandidacyAnnouncement())
