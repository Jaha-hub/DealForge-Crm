from src.backend.application.lead.dtos.custom_fields.views import CustomFieldViewDTO, CustomFieldEnumViewDTO
from src.backend.domain.lead.entity import LeadCustomField


def to_view(field: LeadCustomField) -> CustomFieldViewDTO:
    return CustomFieldViewDTO(
        id=field.id,
        name=field.name.value,
        field_type=field.field_type,
        enums=[
            CustomFieldEnumViewDTO(
                id=e.id,
                value=e.value
            )
            for e in field.enums
        ],
        is_deleted=field.is_deleted,
        created_at=field.created_at,
        updated_at=field.updated_at
    )