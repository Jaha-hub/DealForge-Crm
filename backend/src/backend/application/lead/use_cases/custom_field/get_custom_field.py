from dataclasses import dataclass

from src.backend.application.lead.dtos.custom_fields.get_custom_field import GetCustomFieldCommand, CustomFieldResult
from src.backend.application.lead.dtos.custom_fields.views import CustomFieldViewDTO
from src.backend.application.lead.errors import CustomFieldNotFoundError
from src.backend.application.lead.prejections.custom_field_view import to_view
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class GetCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: GetCustomFieldCommand
    ) -> CustomFieldViewDTO:
        async with self.uow:
            field = await self.uow.custom_fields.get_by_id(cmd.field_id)
            if not field:
                raise CustomFieldNotFoundError()
            if field.is_deleted and not cmd.include_deleted:
                raise CustomFieldNotFoundError()

            return to_view(field)