"""
Main FastAPI application for E-commerce Product Recommender.

This module initializes the FastAPI application with all routers,
middleware, and configuration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uvicorn
import os

from app.core.config import settings
from app.utils.logger import get_logger, main_logger
from app.api import health, products, users, recommendations
from app.models import init_db

# Initialize logger
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for product recommendations with AI-generated explanations",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(recommendations.router)

# Mount static files (frontend)
static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
    # Also mount assets directly to match HTML references
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
else:
    # Fallback: try absolute path from app root
    static_dir = "/app/static"
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
        # Also mount assets directly to match HTML references
        assets_dir = os.path.join(static_dir, "assets")
        if os.path.exists(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Database URL: {settings.database_url}")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down application")


@app.get("/")
async def root():
    """Root endpoint - redirect to frontend."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

