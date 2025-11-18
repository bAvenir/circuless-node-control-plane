import uuid
from sqlalchemy import Text, Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from persistance.database import Base

class ThingDescriptionDB(Base):
    __tablename__ = "thing_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    oid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    td = Column(JSONB, nullable=False)
    # owner
    # allowed or filter 'friends' to give access to "restricted" items
    # privacy
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Text, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    catalog_data = Column(JSONB, nullable=False)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Text, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    dataset_data = Column(JSONB, nullable=False)