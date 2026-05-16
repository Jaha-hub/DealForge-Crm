from enum import StrEnum
from typing import List

from pydantic import BaseModel

from src.backend.application.shared.dtos.pagination import PageRequest
from src.backend.domain.funnel.entity import Funnel


class FunnelSortEnum(StrEnum):
    name_asc = "name:asc"
    name_desc = "name:desc"
    created_at_desc = "created_at:desc"
    created_at_asc = "created_at:asc"

class ListFunnelCommand(BaseModel):
    q: str | None = None
    sort_by: FunnelSortEnum | None = None
    pagination: PageRequest

class ListFunnelResult(BaseModel):
    funnels: List[Funnel]
    page: int
    total_count: int
    total_pages: int