from dataclasses import dataclass
from typing import List

from src.backend.application.lead.dtos.custom_fields.list_custom_field import ListCustomFieldCommand
from src.backend.application.lead.dtos.custom_fields.get_custom_field import CustomFieldResult
from src.backend.application.lead.dtos.custom_fields.views import CustomFieldViewDTO
from src.backend.application.lead.prejections.custom_field_view import to_view
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class ListCustomFieldUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: ListCustomFieldCommand
    ) -> list[CustomFieldViewDTO]:
        async with self.uow:
            fields = await self.uow.custom_fields.list_all(
                field_type=cmd.type,
                include_deleted=cmd.include_deleted
            )
            return [
                to_view(field)
                for field in fields
            ]