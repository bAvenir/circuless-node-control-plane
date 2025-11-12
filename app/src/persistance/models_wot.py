import uuid
from pydantic import BaseModel
from typing import Optional, Dict, Any

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