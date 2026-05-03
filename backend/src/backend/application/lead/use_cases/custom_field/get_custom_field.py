from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.get_custom_field import GetCustomFieldCommand, CustomFieldResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class GetCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: GetCustomFieldCommand,
    ) -> CustomFieldResult:

        async with self.uow:
            field = await self.uow.custom_fields.get_by_id(cmd.id)

            if not field:
                raise ValueError("Custom field not found")

            return CustomFieldResult(
                id=field.id,
                name=field.name,
                type=field.field_type.value,
                enum_values=[e.value for e in field.enums] if field.enums else None
            )