
from sqlalchemy import Column, String, Boolean

from src.backend.infrastructure.db.sqlalchemy.core.mixins import UUIDMixin, TimestampMixin
from src.backend.infrastructure.db.sqlalchemy.core.models import Base


class FunnelModel(Base,UUIDMixin,TimestampMixin):
    __tablename__ = 'funnels'

    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)