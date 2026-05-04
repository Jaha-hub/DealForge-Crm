import hashlib
import secrets
from dataclasses import field, dataclass, replace
from uuid import UUID

from src.backend.domain.shared.entity import BaseEntity
from src.backend.domain.shared.mixins import TimeActionMixin
from src.backend.domain.source.enums.assignment_strategy.enums import AssignmentStrategy
from src.backend.domain.source.enums.source_tupe.enum import SourceType
from src.backend.domain.source.enums.value_objects.form_field_config.value_object import FormFieldConfig
from src.backend.domain.source.enums.value_objects.source_config.errors import NotWebhookSourceError
from src.backend.domain.source.enums.value_objects.source_config.value_object import SourceConfig, WebhookConfig, \
    ManualConfig, PublicFormConfig

_SOURCE_TYPE_TO_CONFIG = {
    SourceType.webhook: WebhookConfig,
    SourceType.manual: ManualConfig,
    SourceType.public_form: PublicFormConfig
}
@dataclass
class Source(BaseEntity, TimeActionMixin):
    name: str
    source_type: SourceType # manual/public_form/webhook
    config: SourceConfig
    is_active: bool = field(default=True)
    is_deleted: bool = field(default=False)

    def __post_init__(self):
        self._ensure_config_matches_type(self.config)

    @classmethod
    def create_webhook(
            cls,
            name: str,
            default_funnel_id: UUID,
            default_stage_id: UUID,
            assignment_strategy: AssignmentStrategy = AssignmentStrategy.manual,  # Enum
            assignment_pool: tuple[UUID, ...] = tuple(),
            field_mapping: dict[str, str] | None = None,
    ):
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        config = WebhookConfig(
            secret_token_hash=token_hash,
            default_funnel_id=default_funnel_id,
            default_stage_id=default_stage_id,
            assignment_strategy=assignment_strategy,
            assignment_pool=assignment_pool,
            field_mapping=field_mapping if field_mapping else {}
        )

        source = cls(
            name=name,
            source_type=SourceType.webhook,
            config=config,
        )
        return source, token

    @classmethod
    def create_public_form(
            cls,
            name: str,
            slug: str,  # Slug
            fields: tuple[FormFieldConfig, ...],  # какие поля будут в форме
            default_funnel_id: UUID,
            default_stage_id: UUID,

            assignment_strategy: AssignmentStrategy,  # Enum
            assignment_pool: tuple[UUID, ...] = tuple(),

            redirect_url: str | None = None,
            success_message: str | None = None,
    ):
        config = PublicFormConfig(
            slug=slug,
            default_funnel_id=default_funnel_id,
            default_stage_id=default_stage_id,
            assignment_strategy=assignment_strategy,
            assignment_pool=assignment_pool,
            redirect_url=redirect_url,
            success_message=success_message,
            fields=fields
        )
        return cls(
            name=name,
            source_type=SourceType.public_form,
            config=config,
        )

    @classmethod
    def create_manual(
            cls,
            name: str
    ):
        config = ManualConfig()
        return cls(
            name=name,
            source_type=SourceType.manual,
            config=config,
        )

    def change_name(
            self,
            name: str
    ):
        self.name = name
        self.touch()

    def change_config(
            self,
            config: SourceConfig
    ):
        self._ensure_config_matches_type(config)
        self.config = config
        self.touch()

    def activate(self):
        self.is_active = True
        self.touch()

    def deactivate(self):
        self.is_active = False
        self.touch()

    def regenerate_secret(self)->str:
        if not isinstance(self.config, WebhookConfig):
            raise
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        self.config = replace(self.config,secret_token_hash=token_hash)
        self.touch()

        return token

    def verify_webhook_token(self, token: str) -> bool:
        if not isinstance(self.config, WebhookConfig):
            raise NotWebhookSourceError()

        import hmac
        expected = hashlib.sha256(token.encode()).hexdigest()
        return hmac.compare_digest(expected, self.config.secret_token_hash)

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.touch()

    def restore(self):
        self.is_deleted = False
        self.touch()

    def _ensure_config_matches_type(self, config: SourceConfig):
        expected_class = _SOURCE_TYPE_TO_CONFIG[self.source_type]
        if not isinstance(config, expected_class):
            raise

