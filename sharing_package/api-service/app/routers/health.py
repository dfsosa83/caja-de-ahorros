"""
Health check endpoints for the Income Prediction API
"""

import time
import psutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import HealthResponse
from app.services.prediction_service import PredictionService
from app.core.logging import get_logger
from app.core.config import get_settings

logger = get_logger("health_router")
settings = get_settings()

# Create router
router = APIRouter(tags=["health"])

# Service startup time
startup_time = time.time()


def get_prediction_service() -> PredictionService:
    """Dependency to get prediction service instance"""
    try:
        return PredictionService()
    except Exception:
        return None


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API service and ML model"
)
async def health_check(
    service: PredictionService = Depends(get_prediction_service)
) -> HealthResponse:
    """
    Comprehensive health check
    
    - **returns**: Service and model health status with uptime information
    """
    try:
        # Calculate uptime
        uptime_seconds = time.time() - startup_time
        
        # Check service health
        service_status = "healthy"
        model_status = "unknown"
        
        if service is not None:
            if service.is_healthy():
                model_status = "loaded"
            else:
                model_status = "error"
                service_status = "degraded"
        else:
            model_status = "not_loaded"
            service_status = "unhealthy"
        
        return HealthResponse(
            status=service_status,
            model_status=model_status,
            version=settings.app_version,
            uptime_seconds=uptime_seconds
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


@router.get(
    "/health/detailed",
    summary="Detailed health check",
    description="Detailed health information including system metrics"
)
async def detailed_health_check(
    service: PredictionService = Depends(get_prediction_service)
) -> dict:
    """
    Detailed health check with system metrics
    
    - **returns**: Comprehensive health information including system resources
    """
    try:
        # Basic health info
        uptime_seconds = time.time() - startup_time
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Service status
        service_healthy = service is not None and service.is_healthy()
        
        return {
            "service": {
                "status": "healthy" if service_healthy else "unhealthy",
                "version": settings.app_version,
                "uptime_seconds": uptime_seconds,
                "uptime_human": f"{uptime_seconds // 3600:.0f}h {(uptime_seconds % 3600) // 60:.0f}m"
            },
            "model": {
                "status": "loaded" if service_healthy else "not_loaded",
                "info": service.get_model_info() if service_healthy else None
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": round((disk.used / disk.total) * 100, 1)
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Detailed health check failed: {str(e)}"
        )


@router.get(
    "/ready",
    summary="Readiness check",
    description="Check if the service is ready to accept requests"
)
async def readiness_check(
    service: PredictionService = Depends(get_prediction_service)
) -> dict:
    """
    Readiness check for load balancers
    
    - **returns**: Simple ready/not ready status
    """
    try:
        is_ready = service is not None and service.is_healthy()
        
        if is_ready:
            return {
                "status": "ready",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="Service not ready"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Readiness check failed: {str(e)}"
        )


@router.get(
    "/live",
    summary="Liveness check",
    description="Check if the service is alive (for container orchestration)"
)
async def liveness_check() -> dict:
    """
    Liveness check for container orchestration
    
    - **returns**: Simple alive status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
