from typing import Protocol
from uuid import UUID

from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.value_objects.field_type.value_object import FieldType


class LeadCustomFieldRepository(Protocol):
    async def add(self, field: LeadCustomField) -> LeadCustomField: ...

    async def update(self, field: LeadCustomField) -> None: ...

    async def remove(self, field: LeadCustomField) -> None: ...

    async def delete(self, field: LeadCustomField) -> None: ...

    async def name_exists(
            self,
            name: str
    ) -> bool: ...

    async def get_by_id(self, id: int) -> LeadCustomField | None: ...

    async def get_all(self) -> list[LeadCustomField]: ...

    async def list_by_ids(self, custom_field_ids: list) -> list[LeadCustomField]: ...

    async def list_all(
            self,
            include_detected: bool = False,
            field_type: FieldType | None = None
    ) -> list[LeadCustomField]: ...

    async def count_values_with_enum_values(
            self,
            enum_id: UUID,
    ) -> int: ...
