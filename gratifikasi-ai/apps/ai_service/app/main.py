"""
FastAPI application entry-point for the AI service.
"""
import structlog
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .api.routes import router
from .core.qdrant_wrapper import ensure_collection

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="Gratifikasi AI Service",
    description="Embedding + similarity search + classification for gratification records",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("ai_service_starting")
    ensure_collection()
    logger.info("ai_service_ready")


@app.get("/health", response_class=JSONResponse)
async def health() -> dict:
    return {"status": "ok"}
