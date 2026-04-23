from src.backend.application.funnel.dtos.update_funnel_stage import UpdateFunnelStageCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel, FunnelStage
from src.backend.domain.funnel.policies.can_update_funnel import CanUpdateFunnelPolicy
from src.backend.domain.user.entity import User


class UpdateFunnelStageUseCase:
    uow: UnitOfWork
    funnel: Funnel
    stage: FunnelStage
    user: User
    async def execute(
            self,
            cmd: UpdateFunnelStageCommand,
    )-> None:
        CanUpdateFunnelPolicy(self.user).enforce()
        async with self.uow:
            self.stage.change(
                name=cmd.name,
                win_probability=cmd.win_probability,
                hex=cmd.hex,
            )
            await self.uow.stages.update_stage(self.stage)
            await self.uow.commit()