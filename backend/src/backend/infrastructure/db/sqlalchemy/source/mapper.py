from uuid import UUID

from src.backend.domain.source.entity import Source
from src.backend.domain.source.enums.assignment_strategy.enums import AssignmentStrategy
from src.backend.domain.source.enums.source_tupe.enum import SourceType
from src.backend.domain.source.enums.value_objects.form_field_config.value_object import FormFieldConfig, FormFieldKind
from src.backend.domain.source.enums.value_objects.source_config.value_object import SourceConfig, PublicFormConfig, \
    WebhookConfig, ManualConfig
from src.backend.infrastructure.db.sqlalchemy.source.models import SourceModel


def serialize_config(config: SourceConfig)-> dict:
    match config:
        case WebhookConfig():
            return {
                "secret_token_hash": config.secret_token_hash,
                "default_funnel_id": str(config.default_funnel_id),
                "default_stage_id": str(config.default_stage_id),
                "assignment_strategy": config.assignment_strategy.value,
                "field_mapping": dict(config.field_mapping),
                "assignment_pool": [str(uid) for uid in config.assignment_pool],
            }
        case PublicFormConfig():
            return {
                "slug": config.slug,
                "fields": [_serialize_form_field(f)for f in config.fields],
                "default_funnel_id": str(config.default_funnel_id),
                "default_stage_id": str(config.default_stage_id),
                "assignment_strategy": config.assignment_strategy.value,
                "assignment_pool": [str(uid) for uid in config.assignment_pool],
                "redirect_url": config.redirect_url,
                "success_message": config.success_message
            }
        case ManualConfig():
            return {}

def _serialize_form_field(field: FormFieldConfig):
    return {
        "kind": field.kind.value,
        "label": field.label,
        "is_required": field.is_required,
        "custom_field_id": str(field.custom_field_id) if field.custom_field_id else None,
        "placeholder": field.placeholder,
    }


def deserialize_config(
        source_type: SourceType,
        raw: dict,
):
    match source_type:
        case SourceType.webhook:
            return WebhookConfig(
                secret_token_hash=raw["secret_token_hash"],
                default_funnel_id=UUID(raw["default_funnel_id"]),
                default_stage_id=UUID(raw["default_stage_id"]),
                assignment_strategy=AssignmentStrategy(raw["assignment_strategy"]),
                assignment_pool=tuple(
                    UUID(uid) for uid in raw["assignment_pool"]
                ),
                field_mapping=dict(raw.get("field_mapping", {})),
            )
        case SourceType.public_form:
            return PublicFormConfig(
                slug=raw["slug"],
                fields=tuple(
                    _deserialize_form_field(f)
                    for f in raw["fields"]
                ),
                default_funnel_id=UUID(raw["default_funnel_id"]),
                default_stage_id=UUID(raw["default_stage_id"]),
                assignment_strategy=AssignmentStrategy(raw["assignment_strategy"]),
                assignment_pool=tuple(
                    UUID(uid) for uid in raw["assignment_pool"]
                ),
                redirect_url=raw["redirect_url"],
                success_message=raw["success_message"],
            )

        case SourceType.manual:
            return ManualConfig()
def _deserialize_form_field(raw:dict)->FormFieldConfig:
    return FormFieldConfig(
        kind=FormFieldKind(raw["kind"]),
        label=raw["label"],
        is_required=raw["is_required"],
        custom_field_id=UUID(raw["custom_field_id"]) if raw.get("custom_field_id") else None,
        placeholder=raw["placeholder"],
    )
def to_model(source: Source) -> SourceModel:
    return SourceModel(
        id=source.id,
        name=source.name,
        source_type=source.source_type,
        config=serialize_config(source.config),
        is_active=source.is_active,
        is_deleted=source.is_deleted,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )

def to_entity(source:SourceModel)->Source:
    source_type = SourceType(source.source_type)
    return Source(
        id=source.id,
        name=source.name,
        source_type=source_type,
        config=deserialize_config(
            source_type=source_type,
            raw=source.config,
        ),
        is_active=source.is_active,
        is_deleted=source.is_deleted,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )