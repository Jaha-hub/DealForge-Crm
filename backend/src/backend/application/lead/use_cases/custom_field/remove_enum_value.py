from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.remove_enum import RemoveEnumValueCommand
from src.backend.application.lead.errors import EnumInUseError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.policies import CanManageCustomField
from src.backend.domain.user.entity import User


@dataclass
class RemoveEnumValueUseCase:
    uow: UnitOfWork
    user: User
    field: LeadCustomField

    async def execute(
            self,
            cmd: RemoveEnumValueCommand
    )-> None:
        CanManageCustomField(self.user).enforce()
        async with self.uow:
            usage_count = await self.uow.custom_fields.count_values_with_enum_values(cmd.enum_id)

            if usage_count > 0:
                raise EnumInUseError()

            self.field.remove_enum(cmd.enum_id)

            await self.uow.custom_fields.update(self.field)
            await self.uow.commit()