import uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class SecurityDefinition(BaseModel):
    scheme: str
    description: Optional[str] = None
    proxy: Optional[str] = None


class Property(BaseModel):
    type: Optional[str] = None
    readOnly: Optional[bool] = None
    writeOnly: Optional[bool] = None
    description: Optional[str] = None
    observable: Optional[bool] = None
    forms: Optional[List[Any]] = None


class Action(BaseModel):
    description: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[Any] = None
    forms: Optional[List[Any]] = None

class ThingDescription(BaseModel):
    oid: Optional[str] = None
    id: Optional[str] = Field(alias='@id')
    context: Optional[Any] = Field(alias='@context')
    type: Optional[str] = Field(alias='@type')
    title: Optional[str]
    description: Optional[str] = None

    security: Optional[List[str]] = None
    securityDefinitions: Optional[Dict[str, SecurityDefinition]] = None

    properties: Optional[Dict[str, Property]] = None
    actions: Optional[Dict[str, Action]] = None
    events: Optional[Dict[str, Any]] = None

    model_config = {
        "populate_by_name": True
    }

    def json_td(self):
        return self.model_dump(by_alias=True, exclude_none=True)

class ThingDescriptionCreate(BaseModel):
    context: Optional[Any] = Field(alias='@context')
    type: Optional[str] = Field(alias='@type')
    title: Optional[str]
    description: Optional[str] = None

    security: Optional[List[str]] = None
    securityDefinitions: Optional[Dict[str, SecurityDefinition]] = None

    properties: Optional[Dict[str, Property]] = None
    actions: Optional[Dict[str, Action]] = None
    events: Optional[Dict[str, Any]] = None

    model_config = {
        "populate_by_name": True
    }

class ThingDescriptionResponse(BaseModel):
    id: int
    oid: uuid.UUID
    # owner: uuid.UUID
    # allowed: ...
    td: Dict[str, Any]
    
    class Config:
        from_attributes = True