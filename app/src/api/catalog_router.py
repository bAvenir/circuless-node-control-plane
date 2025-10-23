import logging
from fastapi import APIRouter
from persistance.models import CatalogResponse
 
 
logger = logging.getLogger(__name__)
catalog_router = APIRouter(prefix="/catalog", tags=["Catalog router"])

@catalog_router.post("/request/", response_model=CatalogResponse)
async def request_catalog():
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
    id: str
):
    ...
    
    
    
# async def update_thing_description(
#     td_id: int,
#     td: ThingDescriptionCreate,
#     db: AsyncSession = Depends(get_db)
# ):