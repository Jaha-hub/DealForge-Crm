from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.create_custom_field import CreateCustomFieldCommand, \
    CreateCustomFieldResult
from src.backend.application.lead.errors import CustomFieldNameAlreadyExistsError, SelectFieldWithoutEnumsError, \
    EnumsNotAllowForNonSelectError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.policies import CanManageCustomField
from src.backend.domain.user.entity import User


@dataclass
class CreateCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: CreateCustomFieldCommand
    ):
        CanManageCustomField(self.user).enforce()
        async with self.uow:
            if await self.uow.custom_fields.name_exists(cmd.name):
                raise CustomFieldNameAlreadyExistsError()
            field = LeadCustomField.create(
                name=cmd.name,
                field_type=cmd.type,
            )

            if cmd.type.is_select:
                for v in cmd.enum_values:
                    field.add_enum(v)

            await self.uow.custom_fields.add(field)
            await self.uow.commit()
            return CreateCustomFieldResult(field_id=field.id)

    @staticmethod
    def _validate_enum_values_match_type(cmd: CreateCustomFieldCommand) -> None:
        if cmd.type.is_select and not cmd.enum_values:
            raise SelectFieldWithoutEnumsError()
        if not cmd.type.is_select and cmd.enum_values:
            raise EnumsNotAllowForNonSelectError()