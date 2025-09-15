"""
Income Prediction API - Main FastAPI Application

This API service wraps the existing income prediction pipeline
to provide REST endpoints for real-time and batch predictions.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.routers import predictions, health
from app.models.schemas import ErrorResponse

# Initialize settings and logging
settings = get_settings()
logger = get_logger("main")

# Global variables for service state
service_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Income Prediction API Service...")
    logger.info(f"📊 Model path: {settings.model_path}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    logger.info(f"📡 Max batch size: {settings.max_batch_size}")
    
    try:
        # Pre-load the prediction service to validate model loading
        from app.services.prediction_service import PredictionService
        service = PredictionService()
        if service.is_healthy():
            logger.info("✅ Model loaded successfully")
        else:
            logger.warning("⚠️ Model loading issues detected")
    except Exception as e:
        logger.error(f"❌ Failed to initialize prediction service: {str(e)}")
        # Don't fail startup, let health checks handle it
    
    logger.info("🎯 Income Prediction API Service started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Income Prediction API Service...")


# Create FastAPI application
app = FastAPI(
    title="Income Prediction API",
    description="""
    ## 🏦 Caja de Ahorros - Income Prediction API
    
    A production-ready REST API for predicting customer income using advanced machine learning models.
    
    ### Features
    - **Single Predictions**: Real-time income predictions for individual customers
    - **Batch Predictions**: Efficient processing of multiple customers
    - **Model Information**: Access to model metadata and feature importance
    - **Health Monitoring**: Comprehensive health checks and system metrics
    - **Input Validation**: Robust data validation with detailed error messages
    
    ### Model Information
    - **Algorithm**: XGBoost with nested cross-validation
    - **Performance**: R² = 0.497, RMSE = $490 USD
    - **Features**: 10 engineered features including financial ratios and employment history
    - **Training Data**: 29,319 customers from Caja de Ahorros
    
    ### Quick Start
    1. Use `/api/v1/predict` for single customer predictions
    2. Use `/api/v1/predict/batch` for multiple customers
    3. Check `/health` for service status
    4. View `/api/v1/model/info` for model details
    
    ### Support
    - **Documentation**: This interactive documentation
    - **Health Checks**: `/health`, `/ready`, `/live` endpoints
    - **Model Info**: `/api/v1/model/info` endpoint
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            details={"path": str(request.url.path)} if settings.debug else None
        ).dict()
    )


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(health.router)
app.include_router(predictions.router)


# Root endpoint
@app.get(
    "/",
    summary="API Information",
    description="Get basic information about the Income Prediction API"
)
async def root():
    """
    API root endpoint with basic information
    """
    uptime_seconds = time.time() - service_start_time
    
    return {
        "service": "Income Prediction API",
        "version": settings.app_version,
        "status": "running",
        "uptime_seconds": round(uptime_seconds, 2),
        "documentation": "/docs",
        "health_check": "/health",
        "model_info": "/api/v1/model/info",
        "endpoints": {
            "single_prediction": "/api/v1/predict",
            "batch_prediction": "/api/v1/predict/batch",
            "health": "/health",
            "ready": "/ready",
            "live": "/live"
        },
        "description": "REST API for predicting customer income using ML models"
    }


# Custom OpenAPI schema
def custom_openapi():
    """Custom OpenAPI schema with additional metadata"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Income Prediction API",
        version=settings.app_version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom metadata
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Starting server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
