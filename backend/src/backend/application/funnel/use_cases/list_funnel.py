from src.backend.application.funnel.dtos.list_funnel import ListFunnelCommand
from src.backend.application.shared.dtos.pagination import PageResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.user.entity import User


class ListFunnelUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
            self,
            cmd: ListFunnelCommand,
    )-> PageResult[Funnel]:
        async with self.uow:
            result = await self.uow.funnels.get_funnels(cmd)
            return result