from typing import Protocol

from src.backend.application.funnel.repository import FunnelRepository, FunnelStageRepository
from src.backend.application.lead.repository import LeadCustomFieldRepository, LeadRepository
from src.backend.application.source.repository import SourceRepository
from src.backend.application.user.repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    funnels: FunnelRepository
    stages: FunnelStageRepository
    custom_fields: LeadCustomFieldRepository
    source: SourceRepository
    leads: LeadRepository
    async def commRepositoryit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def commit(self): ...