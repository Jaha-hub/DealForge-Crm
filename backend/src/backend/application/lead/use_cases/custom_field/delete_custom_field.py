from dataclasses import dataclass
from uuid import UUID

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.user.entity import User


@dataclass
class DeleteCustomFieldUseCase:
    uow: UnitOfWork
    user: User
    custom_field: LeadCustomField

    async def execute(
            self
    )->None:
        async with self.uow:
            self.custom_field.delete()
            await self.custom_field.update(self.custom_field)
            await self.uow.commit()