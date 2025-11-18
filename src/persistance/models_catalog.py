"""
Dataspace Protocol - Pydantic Data Models
Implementation based on Dataspace Protocol 2025-1 specification
"""

from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, HttpUrl
from datetime import datetime
from enum import Enum



"""
Dataspace Protocol - Pydantic Data Models
Implementation based on Dataspace Protocol 2025-1 specification
This file includes models for catalog endpoints responses.
"""


# Test catalog request
class Constraint(BaseModel):
    """Reprezentuje constraint v rámci permission."""
    leftOperand: str
    operator: str
    rightOperand: str


class Permission(BaseModel):
    """Reprezentuje permission s action a constraints."""
    action: str
    constraint: Optional[list[Constraint]] = None


class Policy(BaseModel):
    """Reprezentuje policy (Offer) s ID, type a permissions."""
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    permission: Optional[list[Permission]] = None

    class Config:
        populate_by_name = True


class Distribution(BaseModel):
    """Reprezentuje distribuciu datasetu."""
    type: str = Field(alias="@type")
    format: str
    accessService: str

    class Config:
        populate_by_name = True


class Dataset(BaseModel):
    """Reprezentuje dataset s policies a distributions."""
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    hasPolicy: Optional[list[Policy]] = None
    distribution: Optional[list[Distribution]] = None

    class Config:
        populate_by_name = True


class DataService(BaseModel):
    """Reprezentuje data service s endpoint URL."""
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    endpointURL: str

    class Config:
        populate_by_name = True


class CatalogResponse(BaseModel):
    """Hlavný response model pre catalog endpoint."""
    context: list[str] = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    participantId: str
    service: Optional[list[DataService]] = None
    dataset: list[Dataset] = []  # Môže byť prázdny list

    class Config:
        populate_by_name = True


# Test catalog request

# Test dataset response

class Constraint(BaseModel):
    leftOperand: str
    operator: str
    rightOperand: str

class Permission(BaseModel):
    action: str
    constraint: Optional[list[Constraint]] = None

class Policy(BaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    permission: Optional[list[Permission]] = None

    class Config:
        populate_by_name = True

class DataService(BaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    endpointURL: str

    class Config:
        populate_by_name = True


class Distribution(BaseModel):
    type: str = Field(alias="@type")
    format: str
    accessService: DataService

    class Config:
        populate_by_name = True


class DatasetResponse(BaseModel):
    context: list[str] = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    hasPolicy: Optional[list[Policy]] = None
    distribution: Optional[list[Distribution]] = None

    class Config:
        populate_by_name = True

# Test dataset response