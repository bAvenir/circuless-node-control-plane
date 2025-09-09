from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router as api_router
from utils.config import settings
from core.database import engine, Base

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="CIRCULess Node Control Plane",
    version=settings.APP_VERSION,
)

# Include API routes
app.include_router(api_router)

# Root endpoint for health check or basic info
@app.get("/")
async def root():
    return {"message": "Welcome to the microservice!"}
