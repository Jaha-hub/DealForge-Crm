from datetime import datetime
from typing import Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from src.backend.application.source.dtos.create_source import FormFieldDTO
from src.backend.domain.source.enums.assignment_strategy.enums import AssignmentStrategy
from src.backend.domain.source.enums.source_tupe.enum import SourceType


class GetSourceCommand(BaseModel):
    source_id: UUID


class GetWebhookConfigDTO(BaseModel):
    type: Literal[SourceType.webhook] = SourceType.webhook
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategy = AssignmentStrategy.manual  # Enum
    field_mapping: dict[str, str] = Field(default_factory=dict)
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)


class GetPublicFormConfigDTO(BaseModel):
    type: Literal[SourceType.public_form] = SourceType.public_form
    slug: str # Slug
    fields: list[FormFieldDTO]
    default_funnel_id: UUID
    default_stage_id: UUID
    assignment_strategy: AssignmentStrategy = AssignmentStrategy.manual  # Enum
    assignment_pool: tuple[UUID, ...] = Field(default_factory=tuple)
    redirect_url: str | None = None
    success_message: str | None = None


class GetManualConfigDTO(BaseModel):
    type: Literal[SourceType.manual] = SourceType.manual


GetSourceConfigDTO = Annotated[
    Union[GetWebhookConfigDTO, GetManualConfigDTO, GetPublicFormConfigDTO],
    Field(discriminator="type")
]

class GetSourceResult(BaseModel):
    id: UUID
    name: str
    type: SourceType
    config: GetSourceConfigDTO
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime