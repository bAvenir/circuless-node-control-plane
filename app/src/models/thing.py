import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, Dict, Any

Base = declarative_base()

class ThingDescriptionDB(Base):
    __tablename__ = "thing_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    oid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    td = Column(JSONB, nullable=False)

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
    td: Dict[str, Any]
    
    class Config:
        from_attributes = True