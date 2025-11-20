from contextlib import asynccontextmanager
import time
import uuid
from fastapi import FastAPI
from api.routes import router_api as router_main
from persistance.database import engine
from utils.config import settings
from utils.lifecycle import initialize, shutdown
from utils.otel_config import Otel
from utils.logs import logger, request_id_var, log_with_context

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code — runs before the app starts handling requests
    await initialize(app, otel)
    yield
    # Shutdown code — runs when the app is shutting down
    await shutdown(otel)
    print("Lifespan shutdown: cleaning up resources")

# Set up Open telemetry
otel = Otel(settings.OTEL_ENABLED)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="CIRCULess Node Control Plane",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Set up telemetry
otel.start_telemetry(app, engine)

# Include API routes
app.include_router(router_main)

# Root endpoint for health check or basic info
@app.get("/")
async def root():
    return {"message": "Welcome to the microservice!"}

@app.middleware("http")
async def logging_middleware(request, call_next):
    """
    Middleware to log all requests and add request ID to context
    """
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    
    # Log incoming request
    log_with_context(
        logger,
        "info",
        "Incoming request",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else "unknown"
    )
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log successful response
        log_with_context(
            logger,
            "info",
            "Request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(process_time * 1000, 2)
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        
        # Log error
        log_with_context(
            logger,
            "error",
            f"Request failed: {str(e)}",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            duration_ms=round(process_time * 1000, 2),
            error_type=type(e).__name__
        )
        
        # Re-raise the exception
        raise