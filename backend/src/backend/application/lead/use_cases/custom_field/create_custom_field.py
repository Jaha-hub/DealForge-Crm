from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.create_custom_fields import CreateCustomFieldCommand
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.value_objects.field_type.value_object import FieldType
from src.backend.domain.user.entity import User


@dataclass
class CreateCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: CreateCustomFieldCommand
    ):
        # user админом либо директор
        async with self.uow:
            field = LeadCustomField.create(
                name=cmd.name,
                type=cmd.type,
            )

            if cmd.type.is_select:
                if not cmd.enum_values:
                    raise
                for v in cmd.enum_values:
                    field.add_enum(v)

            await self.uow.custom_fields.add(field)
            await self.uow.commit()
            return