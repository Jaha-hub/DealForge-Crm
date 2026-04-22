from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.funnel.entity import Funnel
from src.backend.domain.funnel.policies.can_delete import CanDeleteFunnelPolicy
from src.backend.domain.user.entity import User


@dataclass
class DeleteFunnelUseCase:
    uow: UnitOfWork
    user: User
    funnel: Funnel

    async def execute(self) -> None:
        CanDeleteFunnelPolicy(self.user).enforce()
        async with self.uow:

            self.funnel.delete()

            # 2. Передача сущности в репозиторий для фиксации изменений в БД
            await self.uow.funnels.delete_funnel(self.funnel)

            # 3. Завершение транзакции
            await self.uow.commit()