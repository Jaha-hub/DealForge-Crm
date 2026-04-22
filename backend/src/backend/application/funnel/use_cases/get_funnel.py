from dataclasses import dataclass

from src.backend.application.funnel.dtos.get_funnel import GetFunnelCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User


@dataclass
class GetFunnelUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: GetFunnelCommand,
    )-> Funnel:
        async with self.uow:
            funnel_id = cmd.funnel_id
            funnel = await self.uow.funnels.get_funnel_by_id(funnel_id)
            if not funnel:
                raise
            return funnel