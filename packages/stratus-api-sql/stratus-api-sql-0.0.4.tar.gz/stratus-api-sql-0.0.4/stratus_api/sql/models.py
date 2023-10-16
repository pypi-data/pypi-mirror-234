from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime, Boolean, ForeignKey, Index, inspect
from sqlalchemy.dialects.postgresql import UUID, JSON, ARRAY
from datetime import datetime
import uuid

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, nullable=False)
    active = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
