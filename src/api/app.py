import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.db import MongoDB
from src.api.schemas import HealthCheckResponse
from src.config.logging import get_logger, setup_logging
from src.config.settings import get_settings

setup_logging()
settings = get_settings()
logger = get_logger("fastapi")
mongodb = MongoDB()


async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI application."""

    # Startup event
    logger.info("Starting up FastAPI application")
    await mongodb.connect()
    yield
    # Shutdown event
    logger.info("Shutting down FastAPI application")
    await mongodb.close()


app = FastAPI(
    title="YouTube WebSub Pipeline API",
    version="0.0.1",
    description="API for the YouTube WebSub Pipeline application",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to calculate and log request processing time."""

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    # Add timing header to response
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

    # Log the request timing
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )

    return response


@app.get("/health", tags=["Health"])
async def health_check() -> HealthCheckResponse:
    """Check the health of all the services."""

    mongo_health_info = await mongodb.is_healthy()

    services_status = [
        {
            "name": "MongoDB",
            "status": mongo_health_info["status"],
            "details": mongo_health_info["details"],
        }
    ]

    overall_status = (
        "healthy" if all(s["status"] == "healthy" for s in services_status) else "unhealthy"
    )

    response = HealthCheckResponse(
        status=overall_status,
        uptime=time.perf_counter(),
        services=[s for s in services_status],
        timestamp=time.time(),
    )

    return response
