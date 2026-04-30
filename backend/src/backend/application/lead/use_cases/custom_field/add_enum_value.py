from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.add_enum_value import AddEnumValueCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.user.entity import User


@dataclass
class AddEnumValueUseCase:
    uow: UnitOfWork
    user: User
    custom_field: LeadCustomField

    async def execute(
            self,
            cmd: AddEnumValueCommand
    )->None:
        async with self.uow:
            self.custom_field.add_enum(cmd.value)
            await self.uow.custom_fields.update(self.custom_field)
            await self.uow.commit()

#RemoveEnumValueUseCase
#DeleteCustomUseCase