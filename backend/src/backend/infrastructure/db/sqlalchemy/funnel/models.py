from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.backend.infrastructure.db.sqlalchemy.core.mixins import UUIDMixin, TimeStampMixin
from src.backend.infrastructure.db.sqlalchemy.core.models import Base


class FunnelModel(Base,UUIDMixin,TimeStampMixin):
    __tablename__ = 'funnels'

    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

class FunnelStageModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "funnel_stages"
    funnel_id = Column(UUID(as_uuid=True), ForeignKey("funnels.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    win_probability = Column(Integer, nullable=False)
    hex = Column(String(7), nullable=False)
    order = Column(Integer, nullable=False)
    is_archived = Column(Boolean, nullable=False, default=False)
    kind = Column(String(100), nullable=True, default="initial")