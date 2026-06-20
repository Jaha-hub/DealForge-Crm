from sqlalchemy import Column, String, Boolean, CheckConstraint, Index, text, ForeignKey
from uuid import UUID

from src.backend.infrastructure.db.sqlalchemy.core.mixins import TimeStampMixin, UUIDMixin
from src.backend.infrastructure.db.sqlalchemy.core.models import Base


class LeadCustomFieldModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "lead_custom_fields"

    name = Column(String(512))
    field_type = Column(String(20))
    is_deleted = Column(Boolean, default=False)
    # name VARCHAR(255) CHECK
    __table_args__ = (
        CheckConstraint(
            "field_type IN ('text','number','date','select_one','select_many','boolean')",
            name="ck_lead_custom_fields_type",
        ),
        Index(
            "uq_lead_custom_fields_active",
            "name",
            unique=True,
            postgresql_where=text("is_deleted = FALSE"),
        ),
    )
class LeadCustomFieldEnumModel(Base, UUIDMixin):
    __tablename__ = "lead_custom_field_enums"

    custom_field_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lead_custom_fields.id", ondelete="CASCADE"),
        nullable=False,
    )
    value = Column(String(255), nullable=False)