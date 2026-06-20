from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import Lead
from src.backend.domain.user.entity import User


@dataclass
class MoveLeadUseCase:
    uow: UnitOfWork
    user: User
    lead: Lead

    async def execute(
            self,
            cmd
    ):
        async with self.uow:
            stage = await self.uow.stages.get_stage_by_id(cmd.stage_id)
            if stage is None:
                raise
            if stage.funnel_id != self.lead.funnel_id:
                raise
            if not stage.is_archived:
                raise
            self.lead.move(stage.id)
            await self.uow.leads.update(self.lead)
            await self.uow.commit()