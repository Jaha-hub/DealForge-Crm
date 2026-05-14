from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.update_custom_field import UpdateCustomFieldCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.policies import CanManageCustomField
from src.backend.domain.user.entity import User


@dataclass
class UpdateCustomFieldUseCase:
    uow: UnitOfWork
    user: User
    field: LeadCustomField

    async def execute(
        self,
        cmd: UpdateCustomFieldCommand
    ) -> None:
        CanManageCustomField(self.user).enforce()

        async with self.uow:
            self.field.rename(cmd.name)

            await self.uow.custom_fields.update(self.field)
            await self.uow.commit()
