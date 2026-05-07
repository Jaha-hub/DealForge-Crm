from dataclasses import dataclass, replace
from uuid import UUID

from src.backend.application.funnel.errors import FunnelNotFoundError, StageNotFoundError, StageNotInFunnelError
from src.backend.application.lead.errors import CustomFieldError, SlugAlreadyExistsError, AssigmentPoolInvalidRoleError, \
    AssigmentPoolMemberInactiveError, AssigmentPoolMemberNotFoundError
from src.backend.application.shared.interfaces.uow import UnitOfWork
from src.backend.application.source.dtos.create_source import FormFieldDTO
from src.backend.application.source.dtos.update_source import UpdateSourceCommand, UpdateSourceConfigDTO, \
    UpdateWebhookConfigDTO, UpdateManualConfigDTO, UpdatePublicFormConfigDTO
from src.backend.domain.source.entity import Source
from src.backend.domain.source.enums.value_objects.form_field_config.value_object import FormFieldConfig, FormFieldKind
from src.backend.domain.source.enums.value_objects.source_config.value_object import SourceConfig, WebhookConfig, \
    PublicFormConfig
from src.backend.domain.user.entity import User


@dataclass
class UpdateSourceUseCase:
    uow: UnitOfWork
    user: User
    source: Source

    async def execute(
            self,
            cmd: UpdateSourceCommand,
    )->None:
        async with self.uow:
            if cmd.name is not None:
                self.source.change_name(cmd.name)
            if cmd.config is not None:
                if cmd.config.type != self.source.config_type:
                    raise CannotChangeSourceTypeError()
                new_config = await self._build_updated_config(self.source, cmd.config)
                if new_config is not None:
                    self.source.change_config(new_config)
            await self.uow.source.update(self.source)
            await self.uow.commit()

    async def _build_updated_config(
            self,
            source: Source,
            patch: UpdateSourceConfigDTO
    )->SourceConfig|None:
        match patch:
            case UpdateWebhookConfigDTO():
                config = await self._update_webhook_config(source.config, patch)
                return config
            case UpdateManualConfigDTO():
                return None
            case UpdatePublicFormConfigDTO():
                config = await self._update_public_form(source, patch)
                return config
    async def _update_webhook_config(
            self,
            current: WebhookConfig,
            patch: UpdateWebhookConfigDTO
    ):
        changes = patch.model_dump(exclude_unset=True, exclude={"type"})

        if not changes:
            return current

        new_funnel_id = changes.get("default_funnel_id",current.default_funnel_id)
        new_stage_id = changes.get("default_stage_id",current.default_stage_id)

        if "default_funnel_id" in changes or "default_stage_id" in changes:
            await self._ensure_funnel_and_stage_valid(new_funnel_id, new_stage_id)

        if "assignment_pool" in changes:
            await self._ensure_assignment_pool(changes["assignment_pool"])
            changes["assignment_pool"] = tuple(changes["assignment_pool"])

        return replace(current, **changes)

    async def _update_public_form(
            self,
            source: Source,
            patch: UpdatePublicFormConfigDTO
    ):
        current: PublicFormConfig = source.public_form
        changes = patch.model_dump(exclude_unset=True, exclude={"type"})
        if not changes:
            return current

        if "slug" in changes and changes["slug"] != current.slug:
            await self._ensure_slug_unique(changes["slug"])

        new_funnel_id = changes.get("default_funnel_id", current.default_funnel_id)
        new_stage_id = changes.get("default_stage_id", current.default_stage_id)

        if "default_funnel_id" in changes or "default_stage_id" in changes:
            await self._ensure_funnel_and_stage_valid(new_funnel_id, new_stage_id)

        if "assignment_pool" in changes:
            await self._ensure_assignment_pool(changes["assignment_pool"])
            changes["assignment_pool"] = tuple(changes["assignment_pool"])

        if 'fields' in changes:
            new_fields = patch.fields
            await self._ensure_custom_fields(list(new_fields))
            changes["fields"] = tuple(
                FormFieldConfig(
                    kind=f.kind,
                    label=f.label,
                    is_required=f.is_required,
                    custom_field_id=f.custom_field_id,
                    placeholder=f.placeholder,
                )
                for f in new_fields
            )

        return replace(current, **changes)

    async def _ensure_funnel_and_stage_valid(
            self,
            funnel_id: UUID,
            stage_id: UUID,
    ):
        funnel = await self.uow.funnels.get_funnel_by_id(funnel_id)
        if not funnel or funnel.is_deleted:
            raise FunnelNotFoundError()

        stage = await self.uow.stages.get_stage_by_id(stage_id)
        if not stage:
            raise StageNotFoundError()

        if stage.funnel_id != funnel_id:
            raise StageNotInFunnelError()

    async def _ensure_assignment_pool(
            self,
            assignment_pool: list[UUID]
    ):
        if len(assignment_pool) == 0:
            return

        users = await self.uow.users.list_by_ids(assignment_pool)
        existing_ids = {u.id for u in users}

        for uid in existing_ids:
            if uid not in assignment_pool:
                raise AssigmentPoolMemberNotFoundError()
        for u in users:
            if not u.is_active:
                raise AssigmentPoolMemberInactiveError()
            if u.role not in [User.role.sales_manager, User.role.consultant]:
                raise AssigmentPoolInvalidRoleError()

    async def _ensure_slug_unique(
            self,
            slug: str,
    ):
        exists = await self.uow.source.exists_slug(slug)
        if exists:
            raise SlugAlreadyExistsError()

    async def _ensure_custom_fields(
            self,
            fields: list[FormFieldDTO]
    ):
        custom_field_ids = [
            f.custom_field_id
            for f in fields
            if f.kind == FormFieldKind.custom_field and f.custom_field_id
        ]
        if not custom_field_ids:
            return

        existing = await self.uow.custom_fields.list_by_ids(custom_field_ids)
        existing_ids = {cf.id for cf in existing if not cf.is_deleted}

        for cf_id in custom_field_ids:
            if cf_id not in existing_ids:
                raise CustomFieldError()