from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import Lead
from src.backend.domain.user.entity import User


@dataclass
class DeleteLeadUseCase:
    uow: UnitOfWork
    user: User
    lead: Lead

    async def execute(self):
        async with self.uow:
            self.lead.delete()
            await self.uow.leads.update(self.lead)
            await self.uow.commit()