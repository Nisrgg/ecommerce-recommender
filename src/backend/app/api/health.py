"""
Health check router for monitoring and debugging.

This module provides endpoints for checking the health and status
of the application and its dependencies.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas import HealthResponse
from app.services.ai_explainer import ai_explainer
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring application status.
    
    Returns:
        Health status including Gemini AI availability
    """
    logger.debug("Health check requested")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        gemini_available=ai_explainer.is_available(),
        version=settings.app_version
    )


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including database connectivity.
    
    Args:
        db: Database session dependency
        
    Returns:
        Detailed health information
    """
    logger.debug("Detailed health check requested")
    
    try:
        # Test database connectivity
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.app_version,
        "database": db_status,
        "gemini_available": ai_explainer.is_available(),
        "cache_enabled": settings.enable_cache,
        "debug_mode": settings.debug
    }

