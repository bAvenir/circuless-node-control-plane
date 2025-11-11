import uuid
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from pydantic import BaseModel
from typing import Optional, Dict, Any
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

# Pydantic models for API
class ThingDescription(BaseModel):
    oid: Optional[uuid.UUID] = None
    title: str
    description: Optional[str] = None
    properties: Dict[str, Any] = {}
    actions: Dict[str, Any] = {}
    events: Dict[str, Any] = {}

class ThingDescriptionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    properties: Dict[str, Any] = {}
    actions: Dict[str, Any] = {}
    events: Dict[str, Any] = {}

class ThingDescriptionResponse(BaseModel):
    id: int
    oid: uuid.UUID
    # owner: uuid.UUID
    # allowed: ...
    td: Dict[str, Any]
    
    class Config:
        from_attributes = True