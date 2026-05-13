from uuid import UUID

from sqlalchemy import select, delete, and_, exists

from src.backend.application.lead.repository import LeadCustomFieldRepository
from src.backend.domain.lead.entity import LeadCustomField
from src.backend.domain.lead.value_objects.field_type.value_object import FieldType
from src.backend.infrastructure.db.sqlalchemy.core.repository.repository import SqlalchemyRepository
from src.backend.infrastructure.db.sqlalchemy.lead.custom_field.mapper import field_to_model, enum_to_model, \
    field_to_entity
from src.backend.infrastructure.db.sqlalchemy.lead.custom_field.models import LeadCustomFieldEnumModel, \
    LeadCustomFieldModel


class SqlAlchemyLeadCustomFieldRepository(SqlalchemyRepository, LeadCustomFieldRepository):
    async def add(self, field: LeadCustomField) -> LeadCustomField:
        instance = field_to_model(field)
        self.session.add(instance)

        self.session.add_all(
            [
                enum_to_model(e)
                for e in field.enums
            ]
        )
        await self.session.flush()
        return field

    async def update(self, field: LeadCustomField) -> None:
        await self.session.merge(field_to_model(field))

        existing_enums = await self._fetch_enums(field.id)
        existing_by_id = {e.id: e for e in existing_enums}
        new_by_id = {e.id: e for e in  field.enums}

        #INSERT
        for enum_id, enum in new_by_id.items():
            self.session.add(enum_to_model(enum))

        for enum_id, enum in new_by_id.items():
            old_enum = existing_by_id.get(enum_id)
            if old_enum is None:
                raise
            if old_enum != enum.value:
                continue
            if old_enum != enum.value:
                await self.session.merge(enum_to_model(enum))

        removed_ids = set(existing_by_id) - set(new_by_id)
        if removed_ids:
            stmt = delete(LeadCustomFieldEnumModel).where(
                LeadCustomFieldEnumModel.id.in_(removed_ids)
            )
            await self.session.execute(stmt)

        await self.session.flush()

    async def name_exists(
            self,
            name: str
    ) -> bool:
        clause = and_(
            LeadCustomFieldModel.name == name,
            LeadCustomFieldModel.is_deleted.is_(False)
        )
        stmt = select(exists().where(clause))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_by_id(self, field_id: UUID) -> LeadCustomField | None:
        stmt = select(LeadCustomFieldModel).where(LeadCustomFieldModel.id == field_id)
        result = await self.session.execute(stmt)
        field = result.scalar_one_or_none()

        if not field:
            return None

        enums = await self._fetch_enums(field.id)
        return field_to_entity(
            field,
            enums
        )

    async def list_all(
            self,
            include_deleted: bool = False,
            field_type: FieldType | None = None
    ) -> list[LeadCustomField]:
        stmt = select(LeadCustomFieldModel)

        if not include_deleted:
            stmt = stmt.where(LeadCustomFieldModel.is_deleted.is_(False))

        if field_type is not None:
            stmt = stmt.where(LeadCustomFieldModel.field_type == field_type)

        stmt = stmt.order_by(LeadCustomFieldModel.created_at.desc())

        result = await self.session.execute(stmt)
        fields = result.scalars().all()

        if not fields:
            return []


    async def _fetch_enums(self, field_id:UUID) -> list[LeadCustomField]:
        stmt = select(LeadCustomFieldEnumModel).where(LeadCustomFieldEnumModel.custom_field_id == field_id)
        result = await self.session.execute(stmt)
        return list[result.scalars().all()]