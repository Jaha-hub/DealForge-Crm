from dataclasses import dataclass

from src.backend.application.funnel.dtos.update_funnel import UpdateFunnelCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.funnel.policies.can_update_funnel import CanUpdateFunnelPolicy
from src.backend.domain.user.entity import User


@dataclass
class UpdateFunnelUseCase:
    uow: UnitOfWork
    user: User
    funnel: Funnel

    async def execute(
            self,
            cmd: UpdateFunnelCommand,
    )-> None:
        CanUpdateFunnelPolicy(self.user).enforce()

        async with self.uow:
            self.funnel.change_name(cmd.name)

            await self.uow.funnels.update_funnel(self.funnel)

            await self.uow.commit()