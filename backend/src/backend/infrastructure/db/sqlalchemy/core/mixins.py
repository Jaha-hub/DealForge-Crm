from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, BigInteger, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class IntIDMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)

class TimeStampMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc),
                        onupdate=lambda: datetime.now(tz=timezone.utc))

class ActiveMixin:
    is_active = Column(Boolean, default=True)