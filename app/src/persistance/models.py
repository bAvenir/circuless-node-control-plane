"""
Dataspace Protocol - Pydantic Data Models
Implementation based on Dataspace Protocol 2025-1 specification
"""

from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, HttpUrl
from datetime import datetime
from enum import Enum


# ============================================================================
# BASE MODELS - Common structures used across the protocol
# ============================================================================


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


class JsonLdBase(BaseModel):
    """Base class for JSON-LD objects with @context, @id, @type"""
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra='allow'
    )
    
    context: Union[Dict[str, str], List[Union[str, Dict[str, str]]]] = Field(
        ..., 
        alias="@context",
        description="JSON-LD context"
    )
    id: str = Field(
        ..., 
        alias="@id",
        description="Unique identifier (IRI/URI)"
    )
    type: Union[str, List[str]] = Field(
        ..., 
        alias="@type",
        description="Type identifier(s)"
    )


# ============================================================================
# ODRL MODELS - Open Digital Rights Language structures
# ============================================================================

class ODRLAction(BaseModel):
    """ODRL Action"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:Action", alias="@type")
    
    # Common actions: use, distribute, reproduce, modify, etc.
    value: Optional[str] = Field(
        None,
        description="Action value (e.g., 'odrl:use', 'odrl:distribute')"
    )


class ODRLConstraint(BaseModel):
    """ODRL Constraint - conditions that must be satisfied"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:Constraint", alias="@type")
    
    left_operand: str = Field(..., alias="odrl:leftOperand")
    operator: str = Field(..., alias="odrl:operator")
    right_operand: Union[str, int, float, bool] = Field(..., alias="odrl:rightOperand")
    
    # For complex constraints
    unit: Optional[str] = Field(None, alias="odrl:unit")
    data_type: Optional[str] = Field(None, alias="odrl:dataType")


class ODRLLogicalConstraint(BaseModel):
    """Logical constraint combining multiple constraints"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:LogicalConstraint", alias="@type")
    
    and_: Optional[List[Union[ODRLConstraint, "ODRLLogicalConstraint"]]] = Field(
        None, alias="odrl:and"
    )
    or_: Optional[List[Union[ODRLConstraint, "ODRLLogicalConstraint"]]] = Field(
        None, alias="odrl:or"
    )
    xone: Optional[List[Union[ODRLConstraint, "ODRLLogicalConstraint"]]] = Field(
        None, alias="odrl:xone"
    )


class ODRLDuty(BaseModel):
    """ODRL Duty - obligation that must be fulfilled"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:Duty", alias="@type")
    
    action: Union[ODRLAction, str] = Field(..., alias="odrl:action")
    constraint: Optional[List[Union[ODRLConstraint, ODRLLogicalConstraint]]] = Field(
        None, alias="odrl:constraint"
    )
    consequence: Optional[List["ODRLDuty"]] = Field(None, alias="odrl:consequence")


class ODRLPermission(BaseModel):
    """ODRL Permission - allowed actions"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:Permission", alias="@type")
    
    action: Union[ODRLAction, str, Dict[str, Any]] = Field(..., alias="odrl:action")
    constraint: Optional[List[Union[ODRLConstraint, ODRLLogicalConstraint]]] = Field(
        None, alias="odrl:constraint"
    )
    duty: Optional[List[ODRLDuty]] = Field(None, alias="odrl:duty")
    
    # Target is inherited from parent in DSP context
    target: Optional[str] = Field(
        None, 
        alias="odrl:target",
        description="Must NOT be set when inside Dataset/Catalog Offer"
    )


class ODRLProhibition(BaseModel):
    """ODRL Prohibition - forbidden actions"""
    id: Optional[str] = Field(None, alias="@id")
    type: str = Field(default="odrl:Prohibition", alias="@type")
    
    action: Union[ODRLAction, str, Dict[str, Any]] = Field(..., alias="odrl:action")
    constraint: Optional[List[Union[ODRLConstraint, ODRLLogicalConstraint]]] = Field(
        None, alias="odrl:constraint"
    )
    
    target: Optional[str] = Field(
        None,
        alias="odrl:target",
        description="Must NOT be set when inside Dataset/Catalog Offer"
    )


class ODRLOffer(JsonLdBase):
    """
    ODRL Offer - defines usage policy
    When inside Catalog/Dataset: target MUST NOT be set (inherited from context)
    When inside negotiation messages: target MUST be set
    """
    type: str = Field(default="odrl:Offer", alias="@type")
    
    permission: Optional[List[ODRLPermission]] = Field(
        default_factory=list, alias="odrl:permission"
    )
    prohibition: Optional[List[ODRLProhibition]] = Field(
        None, alias="odrl:prohibition"
    )
    obligation: Optional[List[ODRLDuty]] = Field(
        None, alias="odrl:obligation"
    )
    
    # Target is context-dependent
    target: Optional[str] = Field(
        None,
        alias="odrl:target",
        description="Dataset ID - set only in negotiation messages"
    )
    
    # ODRL policy attributes
    assigner: Optional[str] = Field(None, alias="odrl:assigner")
    assignee: Optional[str] = Field(None, alias="odrl:assignee")


class ODRLAgreement(JsonLdBase):
    """ODRL Agreement - result of successful negotiation"""
    type: str = Field(default="odrl:Agreement", alias="@type")
    
    target: str = Field(
        ...,
        alias="odrl:target",
        description="Dataset ID - MUST be present in Agreement"
    )
    
    permission: Optional[List[ODRLPermission]] = Field(
        default_factory=list, alias="odrl:permission"
    )
    prohibition: Optional[List[ODRLProhibition]] = Field(
        None, alias="odrl:prohibition"
    )
    obligation: Optional[List[ODRLDuty]] = Field(
        None, alias="odrl:obligation"
    )
    
    # Required for Agreement
    timestamp: datetime = Field(
        ...,
        alias="dspace:timestamp",
        description="Agreement timestamp"
    )
    assigner: str = Field(
        ...,
        alias="odrl:assigner",
        description="Provider participant ID"
    )
    assignee: str = Field(
        ...,
        alias="odrl:assignee",
        description="Consumer participant ID"
    )


# ============================================================================
# DCAT MODELS - Data Catalog Vocabulary structures
# ============================================================================

# Catalog 
# test
# ===== Base Model (ak ho ešte nemáš) =====
class JsonLdBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

# ODRL
class Constraint(JsonLdBase):
    left_operand: str = Field(alias="leftOperand")
    operator: str
    right_operand: str = Field(alias="rightOperand")

class Permission(JsonLdBase):
    action: str
    constraint: List[Constraint] = Field(default_factory=list)

class Policy(JsonLdBase):
    id: str = Field(alias="@id")
    type: str = Field(default="Offer", alias="@type")
    permission: List[Permission] = Field(default_factory=list)

# DCAT
class Distribution(JsonLdBase):
    type: str = Field(default="Distribution", alias="@type")
    format: str
    access_service: str = Field(alias="accessService")

class DCATDatasetTest(JsonLdBase):
    id: str = Field(alias="@id")
    type: str = Field(default="Dataset", alias="@type")
    has_policy: List[Policy] = Field(default_factory=list, alias="hasPolicy")
    distribution: List[Distribution] = Field(default_factory=list)

class DCATDataServiceTest(JsonLdBase):
    id: str = Field(alias="@id")
    type: str = Field(default="DataService", alias="@type")
    endpoint_url: HttpUrl = Field(alias="endpointURL")

class DCATCatalog(JsonLdBase):
    context: List[str] = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(default="Catalog", alias="@type")
    participant_id: str = Field(alias="participantId")
    service: List[DCATDataServiceTest]
    dataset: List[DCATDatasetTest] = Field(default_factory=list)
    
# Test instance

class DCATDataService(JsonLdBase):
    """DCAT Data Service - specifies connector endpoint"""
    type: str = Field(default="dcat:DataService", alias="@type")
    
    endpoint_url: Optional[str] = Field(
        None,
        alias="dcat:endpointURL",
        description="Connector endpoint for negotiation/transfer"
    )
    endpoint_description: Optional[str] = Field(
        None, alias="dcat:endpointDescription"
    )
    serves_dataset: Optional[str] = Field(
        None,
        alias="dcat:servesDataset",
        description="Reference to Dataset ID"
    )
    terms: Optional[str] = Field(
        None,
        alias="dct:terms",
        description="Terms of service"
    )


class DCATDistribution(JsonLdBase):
    """DCAT Distribution - represents accessible form of dataset"""
    type: str = Field(default="dcat:Distribution", alias="@type")
    
    format: Optional[str] = Field(None, alias="dct:format")
    access_service: Optional[Union[DCATDataService, str]] = Field(
        None,
        alias="dcat:accessService",
        description="Data service for accessing this distribution"
    )
    
    # Optional distribution-specific policies
    has_policy: Optional[List[ODRLOffer]] = Field(
        None,
        alias="odrl:hasPolicy",
        description="Distribution-specific policies (optional feature)"
    )


class DCATDataset(JsonLdBase):
    """
    DCAT Dataset with ODRL policies
    Core entity in Dataspace Protocol catalogs
    """
    type: Union[str, List[str]] = Field(default="dcat:Dataset", alias="@type")
    
    # Core metadata
    title: Optional[str] = Field(None, alias="dct:title")
    description: Optional[str] = Field(None, alias="dct:description")
    keyword: Optional[List[str]] = Field(None, alias="dcat:keyword")
    
    # Temporal metadata
    issued: Optional[datetime] = Field(None, alias="dct:issued")
    modified: Optional[datetime] = Field(None, alias="dct:modified")
    
    # DSP requires 1..N policies
    has_policy: List[ODRLOffer] = Field(
        ...,
        alias="odrl:hasPolicy",
        min_length=1,
        description="Usage policies - minimum 1 required"
    )
    
    # DSP requires 1..N distributions
    distribution: List[DCATDistribution] = Field(
        default_factory=list,
        alias="dcat:distribution",
        description="Distribution specifications"
    )
    
    # Additional DCAT properties
    theme: Optional[List[str]] = Field(None, alias="dcat:theme")
    creator: Optional[str] = Field(None, alias="dct:creator")
    publisher: Optional[str] = Field(None, alias="dct:publisher")
    license: Optional[str] = Field(None, alias="dct:license")


class DCATCatalog(JsonLdBase):
    """
    DCAT Catalog - collection of datasets
    Main response structure for Catalog Protocol
    """
    type: str = Field(default="dcat:Catalog", alias="@type")
    
    # Core catalog metadata
    title: Optional[str] = Field(None, alias="dct:title")
    description: Optional[str] = Field(None, alias="dct:description")
    
    # Participant identifier
    participant_id: Optional[str] = Field(
        None,
        alias="dspace:participantId",
        description="Connector participant identifier"
    )
    
    # Datasets (0..N - may be empty based on credentials)
    dataset: List[DCATDataset] = Field(
        default_factory=list,
        alias="dcat:dataset",
        description="Contained datasets"
    )
    
    # DSP requires 1..N data services
    service: Optional[Union[DCATDataService, List[DCATDataService]]] = Field(
        None,
        alias="dcat:service",
        description="Connector service endpoints"
    )
    
    # Additional catalog metadata
    issued: Optional[datetime] = Field(None, alias="dct:issued")
    modified: Optional[datetime] = Field(None, alias="dct:modified")


# ============================================================================
# CONTRACT NEGOTIATION MODELS
# ============================================================================

class ContractNegotiationState(str, Enum):
    """Contract Negotiation state machine states"""
    REQUESTED = "REQUESTED"
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    AGREED = "AGREED"
    VERIFIED = "VERIFIED"
    FINALIZED = "FINALIZED"
    TERMINATED = "TERMINATED"


class ContractRequestMessage(JsonLdBase):
    """
    Contract Request Message - initiates or continues negotiation
    Sent by Consumer
    """
    type: str = Field(default="dspace:ContractRequestMessage", alias="@type")
    
    consumer_pid: Optional[str] = Field(
        None,
        alias="dspace:consumerPid",
        description="Consumer Process ID (for existing negotiation)"
    )
    provider_pid: Optional[str] = Field(
        None,
        alias="dspace:providerPid",
        description="Provider Process ID (for existing negotiation)"
    )
    
    offer: Union[ODRLOffer, str] = Field(
        ...,
        alias="dspace:offer",
        description="ODRL Offer or Offer ID reference"
    )
    
    callback_address: str = Field(
        ...,
        alias="dspace:callbackAddress",
        description="Consumer callback URL for asynchronous messages"
    )
    
    @model_validator(mode='after')
    def validate_offer_target(self):
        """Offer in request message MUST have target"""
        if isinstance(self.offer, ODRLOffer) and not self.offer.target:
            raise ValueError("Offer in ContractRequestMessage must have odrl:target")
        return self


class ContractOfferMessage(JsonLdBase):
    """
    Contract Offer Message - Provider proposes or counter-offers
    Sent by Provider
    """
    type: str = Field(default="dspace:ContractOfferMessage", alias="@type")
    
    consumer_pid: Optional[str] = Field(
        None,
        alias="dspace:consumerPid",
        description="Consumer Process ID (optional for initial message)"
    )
    provider_pid: str = Field(
        ...,
        alias="dspace:providerPid",
        description="Provider Process ID"
    )
    
    offer: ODRLOffer = Field(
        ...,
        alias="dspace:offer",
        description="ODRL Offer with target"
    )
    
    callback_address: Optional[str] = Field(
        None,
        alias="dspace:callbackAddress",
        description="Provider callback URL"
    )
    
    @model_validator(mode='after')
    def validate_offer_target(self):
        """Offer in offer message MUST have target"""
        if not self.offer.target:
            raise ValueError("Offer in ContractOfferMessage must have odrl:target")
        return self


class ContractAgreementMessage(JsonLdBase):
    """
    Contract Agreement Message - Provider confirms agreement
    Sent by Provider when agreeing to contract
    """
    type: str = Field(default="dspace:ContractAgreementMessage", alias="@type")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    agreement: ODRLAgreement = Field(
        ...,
        alias="dspace:agreement",
        description="Complete ODRL Agreement"
    )
    
    callback_address: Optional[str] = Field(
        None, alias="dspace:callbackAddress"
    )


class ContractAgreementVerificationMessage(JsonLdBase):
    """
    Contract Agreement Verification Message
    Sent by Consumer to verify acceptance
    """
    type: str = Field(
        default="dspace:ContractAgreementVerificationMessage",
        alias="@type"
    )
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")


class ContractNegotiationEventType(str, Enum):
    """Event types for negotiation events"""
    FINALIZED = "FINALIZED"
    ACCEPTED = "ACCEPTED"


class ContractNegotiationEventMessage(JsonLdBase):
    """
    Contract Negotiation Event Message
    Used for state transitions like ACCEPTED and FINALIZED
    """
    type: str = Field(
        default="dspace:ContractNegotiationEventMessage",
        alias="@type"
    )
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    event_type: ContractNegotiationEventType = Field(
        ...,
        alias="dspace:eventType",
        description="Type of event (FINALIZED or ACCEPTED)"
    )


class ContractNegotiationTerminationMessage(JsonLdBase):
    """
    Contract Negotiation Termination Message
    Either party can send to terminate negotiation
    """
    type: str = Field(
        default="dspace:ContractNegotiationTerminationMessage",
        alias="@type"
    )
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    code: Optional[str] = Field(
        None,
        alias="dspace:code",
        description="Optional error/termination code"
    )
    reason: Optional[List[Dict[str, Any]]] = Field(
        None,
        alias="dspace:reason",
        description="Optional termination reason details"
    )


class ContractNegotiation(BaseModel):
    """
    Contract Negotiation - response to successful state changes
    """
    model_config = ConfigDict(populate_by_name=True)
    
    context: Union[Dict[str, str], str] = Field(..., alias="@context")
    type: str = Field(default="dspace:ContractNegotiation", alias="@type")
    id: str = Field(..., alias="@id")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    state: ContractNegotiationState = Field(
        ...,
        alias="dspace:state",
        description="Current negotiation state"
    )


class ContractNegotiationError(BaseModel):
    """Contract Negotiation Error response"""
    model_config = ConfigDict(populate_by_name=True)
    
    context: Union[Dict[str, str], str] = Field(..., alias="@context")
    type: str = Field(default="dspace:ContractNegotiationError", alias="@type")
    
    consumer_pid: Optional[str] = Field(None, alias="dspace:consumerPid")
    provider_pid: Optional[str] = Field(None, alias="dspace:providerPid")
    
    code: Optional[str] = Field(None, alias="dspace:code")
    reason: Optional[List[Dict[str, Any]]] = Field(None, alias="dspace:reason")


# ============================================================================
# TRANSFER PROCESS MODELS
# ============================================================================

class TransferState(str, Enum):
    """Transfer Process state machine states"""
    REQUESTED = "REQUESTED"
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class DataAddress(BaseModel):
    """Data Address - transport-specific endpoint information"""
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    
    endpoint_type: str = Field(
        ...,
        alias="dspace:endpointType",
        description="Type of endpoint (e.g., HttpData, S3, etc.)"
    )
    endpoint: Optional[str] = Field(
        None,
        alias="dspace:endpoint",
        description="Endpoint URL or address"
    )
    endpoint_properties: Optional[Dict[str, Any]] = Field(
        None,
        alias="dspace:endpointProperties",
        description="Additional endpoint properties (auth, headers, etc.)"
    )


class TransferRequestMessage(JsonLdBase):
    """
    Transfer Request Message - initiates data transfer
    Sent by Consumer after agreement finalization
    """
    type: str = Field(default="dspace:TransferRequestMessage", alias="@type")
    
    consumer_pid: Optional[str] = Field(
        None,
        alias="dspace:consumerPid",
        description="Consumer Process ID (for existing transfer)"
    )
    provider_pid: Optional[str] = Field(
        None,
        alias="dspace:providerPid",
        description="Provider Process ID (for existing transfer)"
    )
    
    agreement_id: str = Field(
        ...,
        alias="dspace:agreementId",
        description="Reference to finalized contract agreement"
    )
    
    format: Optional[str] = Field(
        None,
        alias="dct:format",
        description="Requested data format"
    )
    
    data_address: Optional[DataAddress] = Field(
        None,
        alias="dspace:dataAddress",
        description="Consumer data address for push transfers"
    )
    
    callback_address: str = Field(
        ...,
        alias="dspace:callbackAddress",
        description="Consumer callback URL"
    )


class TransferStartMessage(JsonLdBase):
    """
    Transfer Start Message - indicates transfer initiation
    Sent by Provider
    """
    type: str = Field(default="dspace:TransferStartMessage", alias="@type")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    data_address: Optional[DataAddress] = Field(
        None,
        alias="dspace:dataAddress",
        description="Provider endpoint for pull transfers (with optional auth)"
    )


class TransferCompletionMessage(JsonLdBase):
    """
    Transfer Completion Message - signals successful completion
    Can be sent by Provider or Consumer
    """
    type: str = Field(default="dspace:TransferCompletionMessage", alias="@type")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")


class TransferSuspensionMessage(JsonLdBase):
    """
    Transfer Suspension Message - temporarily suspends transfer
    Can be sent by Provider or Consumer
    """
    type: str = Field(default="dspace:TransferSuspensionMessage", alias="@type")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    code: Optional[str] = Field(None, alias="dspace:code")
    reason: Optional[List[Dict[str, Any]]] = Field(None, alias="dspace:reason")


class TransferTerminationMessage(JsonLdBase):
    """
    Transfer Termination Message - terminates transfer process
    Can be sent by Provider or Consumer
    """
    type: str = Field(default="dspace:TransferTerminationMessage", alias="@type")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    code: Optional[str] = Field(None, alias="dspace:code")
    reason: Optional[List[Dict[str, Any]]] = Field(None, alias="dspace:reason")


class TransferProcess(BaseModel):
    """Transfer Process - response to successful state changes"""
    model_config = ConfigDict(populate_by_name=True)
    
    context: Union[Dict[str, str], str] = Field(..., alias="@context")
    type: str = Field(default="dspace:TransferProcess", alias="@type")
    id: str = Field(..., alias="@id")
    
    consumer_pid: str = Field(..., alias="dspace:consumerPid")
    provider_pid: str = Field(..., alias="dspace:providerPid")
    
    state: TransferState = Field(
        ...,
        alias="dspace:state",
        description="Current transfer state"
    )


class TransferError(BaseModel):
    """Transfer Process Error response"""
    model_config = ConfigDict(populate_by_name=True)
    
    context: Union[Dict[str, str], str] = Field(..., alias="@context")
    type: str = Field(default="dspace:TransferError", alias="@type")
    
    consumer_pid: Optional[str] = Field(None, alias="dspace:consumerPid")
    provider_pid: Optional[str] = Field(None, alias="dspace:providerPid")
    
    code: Optional[str] = Field(None, alias="dspace:code")
    reason: Optional[List[Dict[str, Any]]] = Field(None, alias="dspace:reason")


# ============================================================================
# VERSION DISCOVERY MODEL
# ============================================================================

class ProtocolVersion(BaseModel):
    """Dataspace Protocol Version information"""
    model_config = ConfigDict(populate_by_name=True)
    
    version: str = Field(
        ...,
        alias="dspace:version",
        description="Version tag (e.g., '2025-1')"
    )
    path: str = Field(
        ...,
        alias="dspace:path",
        description="URL path segment for this version's endpoints"
    )


class ProtocolVersions(BaseModel):
    """Response for version discovery"""
    model_config = ConfigDict(populate_by_name=True)
    
    context: Union[Dict[str, str], str] = Field(..., alias="@context")
    type: str = Field(default="dspace:ProtocolVersions", alias="@type")
    
    protocol_versions: List[ProtocolVersion] = Field(
        ...,
        alias="dspace:protocolVersions",
        min_length=1,
        description="Supported protocol versions"
    )
