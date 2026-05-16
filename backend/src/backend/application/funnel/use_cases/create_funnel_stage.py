import uuid
from dataclasses import dataclass

from src.backend.application.funnel.dtos.create_funnel_stage import CreateFunnelStageCommand, CreateFunnelStageResult
from src.backend.application.funnel.services.stage_ordering import FunnelStageOrderingService
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.funnel.policies.can_create_funnel import CanCreateFunnelPolicy
from src.backend.domain.user.entity import User


@dataclass
class CreateFunnelStageUseCase:
    uow: UnitOfWork
    funnel: Funnel
    ordering: FunnelStageOrderingService
    user: User
    async def execute(
            self,
            cmd: CreateFunnelStageCommand
    ):
        CanCreateFunnelPolicy(self.user).enforce()
        async with self.uow:
            stages = await self.uow.stages.get_funnel_stages(self.funnel.id)

            stage = FunnelStage.create(
                funnel_id=self.funnel.id,
                name=cmd.name,
                win_probability=cmd.win_probability,
                hex=cmd.hex,
            )

            position = cmd.position if cmd.position else len(stages)

            updated_stages = self.ordering.insert(stages, stage,position)

            await self.uow.stages.save_all(updated_stages)
            await self.uow.commit()

            return CreateFunnelStageResult(
                stage_id=stage.id,
            )