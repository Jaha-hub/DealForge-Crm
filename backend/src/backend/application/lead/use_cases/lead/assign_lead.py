from dataclasses import dataclass

from src.backend.application.lead.dtos.lead.assign_lead import AssignLeadCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import Lead
from src.backend.domain.user.entity import User


@dataclass
class AssignLeadUseCase:
    uow: UnitOfWork
    user: User
    lead: Lead

    async def execute(self, cmd: AssignLeadCommand):
        async with self.uow:
            assigned_to = await self.uow.users.get_by_id(cmd.assign_to)
            if not assigned_to or not assigned_to.is_active:
                raise
            self.lead.assing_to(cmd.assigned_to)
            await self.uow.commit()