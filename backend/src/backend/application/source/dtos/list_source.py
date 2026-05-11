from enum import StrEnum

from pydantic import BaseModel, Field

from src.backend.application.shared.dtos.pagination import PageRequest
from src.backend.domain.source.enums.source_tupe.enum import SourceType

class ListSourceSort(StrEnum):
    created_at_desc = "created_at_desc"
    created_at_asc = "created_at_asc"
    name_desc = "name_desc"
    name_asc = "name_asc"

class ListSourceCommand(BaseModel):
    type: SourceType | None = None
    is_active: bool | None = None
    q: str | None = None
    sort: ListSourceSort
    pagination: PageRequest