from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.remove_enum import RemoveEnumValueCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.user.entity import User


@dataclass
class RemoveEnumValueUseCase:
    uow: UnitOfWork
    user: User
    custom_field: LeadCustomField

    async def execute(
            self,
            cmd: RemoveEnumValueCommand
    )-> None:
        async with self.uow:
            self.custom_field.remove_enum(cmd.value)
            await self.uow.custom_fields.update(self.custom_field)
            await self.uow.commit()