from dataclasses import dataclass

from src.backend.application.funnel.dtos.get_funnel_stage import GetFunnelStageCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage


@dataclass
class GetFunnelStageUseCase:
    uow : UnitOfWork
    funnel : Funnel

    async def execute(
            self,
            cmd: GetFunnelStageCommand,
    )->FunnelStage:

        async with self.uow:
            stage = await self.uow.stages.get_stage_by_id(cmd.stage_id)
            if not stage:
                raise
            if stage.funnel_id != cmd.funnel_id:
                raise
            return stage