from dataclasses import dataclass
from typing import List

from src.backend.application.lead.dtos.custom_fields.get_all_custom_fields import GetAllCustomFieldsCommand
from src.backend.application.lead.dtos.custom_fields.get_custom_field import CustomFieldResult
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.user.entity import User


@dataclass
class GetAllCustomFieldsUseCase:
    uow: UnitOfWork
    user: User

    async def execute(
        self,
        cmd: GetAllCustomFieldsCommand,
    ) -> List[CustomFieldResult]:

        async with self.uow:
            fields = await self.uow.custom_fields.get_all()

            result = []

            for field in fields:
                result.append(
                    CustomFieldResult(
                        id=field.id,
                        name=field.name,
                        type=field.field_type.value,
                        enum_values=[
                            e.value for e in field.enums
                        ] if field.enums else None
                    )
                )

            return result