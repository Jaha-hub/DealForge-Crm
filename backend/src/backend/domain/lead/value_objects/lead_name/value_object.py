import re
from dataclasses import dataclass

from src.backend.domain.lead.value_objects.lead_name.errors import \
(
    InvalidLeadNameLengthError,
    UnSupportedLeadNameTypeError
)


@dataclass(frozen=True)
class LeadName:
    """ VO LeadName """
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise UnSupportedLeadNameTypeError()

        if not (2 <= len(self.value) or len(self.value) >= 512):
            raise InvalidLeadNameLengthError()
    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)