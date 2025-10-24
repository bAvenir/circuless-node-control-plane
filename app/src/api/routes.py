import uuid
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from persistance.database import get_db
#from persistance.models import ThingDescriptionCreate, ThingDescriptionResponse
#from persistance.crud import ThingDescriptionCRUD
from api.catalog_router import catalog_router as catalog_router
from api.negotiation_router import negotiation_router as negotiations_router
from api.transfers_router import transfers_router as transfers_router
from persistance.models import VersionResponse

logger = logging.getLogger(__name__)



router = APIRouter(
    prefix="/api/v1",
    tags=["WoT Directory"],
    responses={404: {"description": "Not found"}}
)

router.include_router(catalog_router)
router.include_router(negotiations_router)
router.include_router(transfers_router)

# Exposure of Versions

@router.get("/.well-known/dspace-version", response_model=VersionResponse)
async def get_dspace_version():
    payload = {
        "protocolVersions": [
            {
            "version": "2025-1",
            "path": "/some/path/2025-1",
            "binding": "HTTPS",
            "serviceId": "service-asdf",
            "identifierType": "did:web"
            },
            {
            "version": "2024-1",
            "path": "/some/path/2024-1",
            "binding": "HTTPS",
            "auth": {
                "protocol": "OAuth",
                "version": "2",
                "profile": [
                "authorization_code",
                "refresh_token"
                ]
            },
            "serviceId": "service-asdf",
            "identifierType": "D-U-N-S"

            },
            {
            "version": "2025-1",
            "path": "/different/path/2025-1",
            "binding": "HTTPS",
            "auth": {
                "protocol": "DCP",
                "version": "1.0",
                "profile": [
                "vc11-sl2021/jwt"
                ]
            },
            "serviceId": "service-qwerty"
            }
        ]
        }
    return payload

# @router.post("/things/", response_model=ThingDescriptionResponse)
# async def create_thing_description(
#     td: ThingDescriptionCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Create a new Thing Description"""
#     td_data = td.dict()
#     db_td = await ThingDescriptionCRUD.create(db, td_data)
#     logger.info("Asset succesfuly posted")
#     return db_td

# @router.get("/things/{td_id}", response_model=ThingDescriptionResponse)
# async def get_thing_description(
#     td_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Get Thing Description by ID"""
#     db_td = await ThingDescriptionCRUD.get_by_id(db, td_id)
#     if not db_td:
#         raise HTTPException(status_code=404, detail="Thing Description not found")
#     logger.info("Asset succesfuly retrieved")
#     return db_td

# @router.get("/things/oid/{oid}", response_model=ThingDescriptionResponse)
# async def get_thing_description_by_oid(
#     oid: uuid.UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Get Thing Description by OID"""
#     db_td = await ThingDescriptionCRUD.get_by_oid(db, oid)
#     if not db_td:
#         raise HTTPException(status_code=404, detail="Thing Description not found")
#     logger.info("Asset succesfuly retrieved")
#     return db_td

# @router.get("/things/", response_model=List[ThingDescriptionResponse])
# async def list_thing_descriptions(
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db)
# ):
#     """List all Thing Descriptions"""
#     logger.info("Assets succesfuly retrieved")
#     return await ThingDescriptionCRUD.get_all(db, skip=skip, limit=limit)

# @router.put("/things/{td_id}", response_model=ThingDescriptionResponse)
# async def update_thing_description(
#     td_id: int,
#     td: ThingDescriptionCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Update Thing Description"""
#     td_data = td.dict()
#     db_td = await ThingDescriptionCRUD.update(db, td_id, td_data)
#     if not db_td:
#         raise HTTPException(status_code=404, detail="Thing Description not found")
#     logger.info("Asset succesfuly updated")
#     return db_td

# @router.delete("/things/{td_id}")
# async def delete_thing_description(
#     td_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Delete Thing Description"""
#     success = await ThingDescriptionCRUD.delete(db, td_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Thing Description not found")
#     logger.info("Asset succesfuly deleted")
#     return {"message": "Thing Description deleted successfully"}

# @router.get("/search/", response_model=List[ThingDescriptionResponse])
# async def search_thing_descriptions(
#     field: str,
#     value: str,
#     db: AsyncSession = Depends(get_db)
# ):
#     """Search Thing Descriptions by JSONB field"""
#     results = await ThingDescriptionCRUD.query_jsonb_field(db, field, value)
#     logger.info("Asset succesfuly retrieved")
#     return results