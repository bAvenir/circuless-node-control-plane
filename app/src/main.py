from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router as api_router
from utils.config import settings
from utils.lifecycle import initialize

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code — runs before the app starts handling requests
    initialize()
    yield
    # Shutdown code — runs when the app is shutting down
    print("Lifespan shutdown: cleaning up resources")

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="CIRCULess Node Control Plane",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Include API routes
app.include_router(api_router)

# Root endpoint for health check or basic info
@app.get("/")
async def root():
    return {"message": "Welcome to the microservice!"}
