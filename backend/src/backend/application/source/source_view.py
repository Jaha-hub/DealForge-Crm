from src.backend.application.source.dtos.create_source import FormFieldDTO
from src.backend.application.source.dtos.get_source import GetSourceResult, GetSourceConfigDTO, GetWebhookConfigDTO, \
    GetManualConfigDTO, GetPublicFormConfigDTO
from src.backend.domain.source.entity import Source
from src.backend.domain.source.enums.value_objects.source_config.value_object import WebhookConfig, SourceConfig, \
    ManualConfig, PublicFormConfig


def to_result(
        source: Source
) -> GetSourceResult:
    return GetSourceResult(
        id=source.id,
        name=source.name,
        type=source.sourcetype,
        config=config_to_view(source.config),
        is_active=source.is_active,
        is_deleted=source.is_deleted,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


def config_to_view(config: SourceConfig) -> GetSourceConfigDTO:
    match config:
        case WebhookConfig():
            return GetWebhookConfigDTO(
                default_funnel_id=config.default_funnel_id,
                default_stage_id=config.default_stage_id,
                assignment_strategy=config.assignment_strategy,
                assignment_pool=config.assignment_pool,
                field_mapping=config.field_mapping
            )
        case ManualConfig():
            return GetManualConfigDTO()
        case PublicFormConfig():
            return GetPublicFormConfigDTO(
                slug=config.slug,
                fields=[
                    FormFieldDTO(
                        kind=f.kind,
                        label=f.label,
                        is_required=f.is_required,
                        custom_field_id=f.custom_field_id,
                        placeholder=f.placeholder
                    )
                    for f in config.fields
                ],
                default_funnel_id=config.default_funnel_id,
                default_stage_id=config.default_stage_id,
                assignment_pool=config.assignment_pool,
                assignment_strategy=config.assignment_strategy,
                redirect_url=config.public_base_url
            )