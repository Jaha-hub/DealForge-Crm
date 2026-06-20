from typing import Protocol
from uuid import UUID

from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.domain.lead.entity import LeadCustomField, Lead
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


class LeadRepository(Protocol):
    async def add(self, lead : Lead)-> Lead: ...

    async def get_duplicates(
            self,
            phone: str | None = None,
            email: str | None = None,
            telegram: str | None = None,
    )-> list[Lead]: ...

    async def update(self, lead: Lead) -> None: ...

    async def get_by_id(self, lead_id: UUID) -> Lead | None: ...

    async def is_deleted(self):...