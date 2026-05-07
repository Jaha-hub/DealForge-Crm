from dataclasses import dataclass

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.source.entity import Source
from src.backend.domain.user.entity import User

@dataclass
class DeleteSourceUseCase:
    uow: UnitOfWork
    user: User
    source: Source

    async def execute(self):
        async with self.uow:
            self.source.delete()
            await self.uow.source.update(self.source)
            await self.uow.commit()