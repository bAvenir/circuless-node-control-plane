import logging
from fastapi import APIRouter
from persistance.models import CatalogResponse, DatasetResponse
from pydantic import BaseModel, Field
 
 
logger = logging.getLogger(__name__)
catalog_router = APIRouter(prefix="/catalog", tags=["Catalog router"])


class CatalogRequestMessage(BaseModel):
    """Request model pre catalog endpoint."""
    context: list[str] = Field(alias="@context")
    type: str = Field(alias="@type")
    filter: list = Field(default_factory=list)

    class Config:
        populate_by_name = True
        
        
        
class DatasetRequestMessage(BaseModel):
    """Request model for dataset query."""
    context: list[str] = Field(alias="@context")
    type: str = Field(alias="@type")
    dataset: str

    class Config:
        populate_by_name = True

@catalog_router.post("/request/", response_model=CatalogResponse)
async def request_catalog(msg: CatalogRequestMessage):
    payload = {
        "@context": ["https://w3id.org/dspace/2025/1/context.jsonld"],
        "@id": "urn:uuid:3afeadd8-ed2d-569e-d634-8394a8836d57",
        "@type": "Catalog",
        "participantId": "urn:example:DataProviderA",
        "service": [
            {
                "@id": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                "@type": "DataService",
                "endpointURL": "https://provider-a.com/connector",
            }
        ],
        "dataset": [
            {
                "@id": "urn:uuid:3dd1add8-4d2d-569e-d634-8394a8836a88",
                "@type": "Dataset",
                "hasPolicy": [
                    {
                        "@id": "urn:uuid:3dd1add8-4d2d-569e-d634-8394a8836a88",
                        "@type": "Offer",
                        "permission": [
                            {
                                "action": "use",
                                "constraint": [
                                    {
                                        "leftOperand": "spatial",
                                        "operator": "eq",
                                        "rightOperand": "http://example.org/EU",
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "distribution": [
                    {
                        "@type": "Distribution",
                        "format": "HttpData-PULL",
                        "accessService": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                    }
                ],
            }
        ],
    }
    
    return CatalogResponse.model_validate(payload)
   
    
    
    
    
    

@catalog_router.post("/dataset/{id}") #, response_model=...)
async def query_catalog(
    id: str, msg: DatasetRequestMessage
):
    
    payload = {
        "@context": [
    "https://w3id.org/dspace/2025/1/context.jsonld"
  ],
  "@id": "urn:uuid:3afeadd8-ed2d-569e-d634-8394a8836d57",
  "@type": "Dataset",
  "hasPolicy": [
    {
      "@type": "Offer",
      "@id": "urn:uuid:2828282:3dd1add8-4d2d-569e-d634-8394a8836a88",
      "permission": [
        {
          "action": "use",
          "constraint": [
            {
              "leftOperand": "spatial",
              "rightOperand": "_:EU",
              "operator": "eq"
            }
          ]
        }
      ]
    }
  ],
  "distribution": [
    {
      "@type": "Distribution",
      "format": "HttpData-PULL",
      "accessService": {
        "@id": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
        "@type": "DataService",
        "endpointURL": "https://provider-a.com/connector"
      }
    }
  ]
    }
    
    return DatasetResponse.model_validate(payload)
    
    
    
# async def update_thing_description(
#     td_id: int,
#     td: ThingDescriptionCreate,
#     db: AsyncSession = Depends(get_db)
# ):