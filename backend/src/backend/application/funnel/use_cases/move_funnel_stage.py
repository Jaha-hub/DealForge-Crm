from dataclasses import dataclass

from src.backend.application.funnel.dtos.move_funnel_stage import MoveFunnelStageCommand
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage


@dataclass
class MoveFunnelStageUseCase:
    uow: UnitOfWork
    funnel: Funnel
    stage: FunnelStage
    ordering: FunnelStageOrderingService
    async def execute(
            self,
            cmd: MoveFunnelStageCommand
    )-> None:
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            updated =  self.ordering.move(stages,self.stage, cmd.position)

            await self.uow.stages.save_all(updated)
            await self.uow.commit()