from dataclasses import dataclass
from typing import List

from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import FunnelStage, Funnel


@dataclass
class ListFunnelStageUseCase:
    uow: UnitOfWork
    funnel: Funnel
    ordering: FunnelStageOrderingService
    async def execute(
            self,
    ) -> List[FunnelStage]:
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)
            return self.ordering.normalize(stages)