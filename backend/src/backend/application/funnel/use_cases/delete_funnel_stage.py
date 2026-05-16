from dataclasses import dataclass

from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.funnel.policies.can_delete import CanDeleteFunnelPolicy
from src.backend.domain.user.entity import User


@dataclass
class DeleteFunnelStageUseCase:
    uow: UnitOfWork
    funnel : Funnel
    stage : FunnelStage
    ordering: FunnelStageOrderingService
    user: User
    async def execute(self)-> None:
        CanDeleteFunnelPolicy(self.user).enforce()
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            updated = self.ordering.remove(stages,self.stage)

            await self.uow.stages.delete_stage(self.stage)
            await self.uow.stages.save_all(updated)
            await self.uow.commit()