import logging
from fastapi import APIRouter
from persistance.models_catalog import CatalogResponse, DatasetResponse
from pydantic import BaseModel, Field
from persistance.crud_catalog import get_dataset
from persistance.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)
router_catalog = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
    responses={404: {"description": "Not found"}},
)


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


@router_catalog.post("/request/", response_model=CatalogResponse)
async def request_catalog(msg: CatalogRequestMessage):
    payload = {
        "@context": ["https://w3id.org/dspace/2025/1/context.jsonld"],
        "@id": "urn:uuid:3afeadd8-ed2d-569e-d634-8394a8836d57",
        "@type": "Catalog",
        "participantId": "urn:kezmarok:city-data-provider",
        "service": [
            {
                "@id": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                "@type": "DataService",
                "endpointURL": "https://egov.kezmarok.sk/dataspace-connector",
            }
        ],
        "dataset": [
            {
                "@id": "urn:uuid:kezmarok-streets-dataset-2025",
                "@type": "Dataset",
                "title": "Register ulíc mesta Kežmarok",
                "description": "Kompletný zoznam ulíc a verejných priestranstiev v meste Kežmarok",
                "keyword": ["ulice", "streets", "Kežmarok", "verejné priestranstvá"],
                "issued": "2025-01-15",
                "modified": "2025-10-20",
                "license": "https://creativecommons.org/licenses/by-nd/4.0/",
                "hasPolicy": [
                    {
                        "@id": "urn:uuid:policy-streets-kezmarok",
                        "@type": "Offer",
                        "permission": [
                            {
                                "action": "use",
                                "constraint": [
                                    {
                                        "leftOperand": "spatial",
                                        "operator": "eq",
                                        "rightOperand": "http://publications.europa.eu/resource/authority/country/SVK",
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "distribution": [
                    {
                        "@type": "Distribution",
                        "format": "application/json",
                        "accessURL": "https://egov.kezmarok.sk/Default.aspx?NavigationState=160:0::plac1280:_144055_5_8",
                        "accessService": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                    },
                    {
                        "@type": "Distribution",
                        "format": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "accessURL": "https://egov.kezmarok.sk/Default.aspx?NavigationState=160:0::plac1280:_144055_5_32",
                        "accessService": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                    },
                ],
            },
            {
                "@id": "urn:uuid:kezmarok-contracts-dataset-2025",
                "@type": "Dataset",
                "title": "Zoznam zmlúv mesta Kežmarok",
                "description": "Register zverejnených zmlúv a dodatkov uzatvorených mestom Kežmarok podľa zákona o slobodnom prístupe k informáciám",
                "keyword": [
                    "zmluvy",
                    "contracts",
                    "Kežmarok",
                    "verejné obstarávanie",
                    "transparency",
                ],
                "issued": "2025-01-10",
                "modified": "2025-10-24",
                "license": "https://creativecommons.org/licenses/by-nd/4.0/",
                "hasPolicy": [
                    {
                        "@id": "urn:uuid:policy-contracts-kezmarok",
                        "@type": "Offer",
                        "permission": [
                            {
                                "action": "use",
                                "constraint": [
                                    {
                                        "leftOperand": "spatial",
                                        "operator": "eq",
                                        "rightOperand": "http://publications.europa.eu/resource/authority/country/SVK",
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "distribution": [
                    {
                        "@type": "Distribution",
                        "format": "application/json",
                        "accessURL": "https://egov.kezmarok.sk/Default.aspx?NavigationState=778:0::plac1889:_144101_5_8",
                        "accessService": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                    },
                    {
                        "@type": "Distribution",
                        "format": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "accessURL": "https://egov.kezmarok.sk/Default.aspx?NavigationState=778:0::plac1889:_144101_5_32",
                        "accessService": "urn:uuid:4aa2dcc8-4d2d-569e-d634-8394a8834d77",
                    },
                ],
            },
        ],
    }

    return CatalogResponse.model_validate(payload)


@router_catalog.post("/dataset/{id}")
async def query_catalog(
    id: str, msg: DatasetRequestMessage, db: AsyncSession = Depends(get_db)
):
    dataset = await get_dataset(db, id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Extract the JSONB data from the dataset_data column
    return DatasetResponse.model_validate(dataset.dataset_data)
    # return dataset.dataset_data
