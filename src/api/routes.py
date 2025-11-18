import logging
from fastapi import APIRouter, Response, status, Depends

#from persistance.models import ThingDescriptionCreate, ThingDescriptionResponse
#from persistance.crud import ThingDescriptionCRUD
from api.routes_catalog import router_catalog
from api.routes_wot import router_wot
from persistance.crud_health import check_postgres
from persistance.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
# from api.negotiation_router import negotiation_router as negotiations_router
# from api.transfers_router import transfers_router as transfers_router
from persistance.models import VersionResponse, HealthCheckResponse
from datetime import datetime

logger = logging.getLogger(__name__)

router_api = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}}
)

router_api.include_router(router_catalog)
router_api.include_router(router_wot)

# Health checks

@router_api.get("/health", 
                responses={
                    200: {"description": "Service is healthy"},
                    503: {"description": "Service is unhealthy"}
                    },
                tags=["Main"])
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router_api.get("/health/ready",
                response_model=HealthCheckResponse,
                responses={
                    200: {"description": "Service is healthy"},
                    503: {"description": "Service is unhealthy"}
                    }, 
                tags=["Main"])
async def readiness_check(response: Response, db: AsyncSession = Depends(get_db)):
    """
    Readiness check including dependencies
    Returns 503 if any dependency is unhealthy
    """
    checks = {
        "app": {"status": "healthy"}
    }
    
    # Check database if engine provided
    if db:
        checks["postgres"] = await check_postgres(db)
    
    # Determine overall health
    all_healthy = all(
        check.get("status") == "healthy" 
        for check in checks.values()
    )
    
    if not all_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }

# Exposure of Versions

@router_api.get("/.well-known/dspace-version", response_model=VersionResponse, tags=["Main"])
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