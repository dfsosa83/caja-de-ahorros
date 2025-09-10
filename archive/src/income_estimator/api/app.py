"""
FastAPI application for the Income Estimator ML project.
"""

import time
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

from ..config import get_config
from ..logger import get_logger, log_api_request, log_error
from .models import (
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
)
from .middleware import RateLimitMiddleware

# Initialize logger
logger = get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "predictions_total",
    "Total number of predictions made",
    ["method", "endpoint", "status_code"]
)
REQUEST_DURATION = Histogram(
    "prediction_duration_seconds",
    "Prediction processing time"
)
ERROR_COUNT = Counter(
    "errors_total",
    "Total number of errors",
    ["error_type"]
)

# Get configuration
config = get_config()

# Create FastAPI app
app = FastAPI(
    title="Income Estimator ML API",
    description="A production-ready machine learning API for income estimation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=config.api.cors_methods,
    allow_headers=config.api.cors_headers,
)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=config.api.rate_limit_requests,
    window_seconds=config.api.rate_limit_window,
)

# Global predictor instance (will be initialized on startup)
predictor = None


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log the request
        log_api_request(
            method=request.method,
            endpoint=str(request.url.path),
            status_code=response.status_code,
            response_time=process_time,
        )
        
        # Update Prometheus metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.observe(process_time)
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        
        # Log the error
        log_error(e, context={"request_path": str(request.url.path)})
        ERROR_COUNT.labels(error_type=type(e).__name__).inc()
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    global predictor
    
    logger.info("Starting Income Estimator ML API...")
    
    try:
        # Initialize the predictor
        from ..models.predictor import ModelPredictor
        predictor = ModelPredictor(config)
        
        logger.info("API startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to start API: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down Income Estimator ML API...")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if predictor is available
        model_status = "healthy" if predictor and predictor.is_ready() else "unhealthy"
        
        return HealthResponse(
            status="healthy",
            model_status=model_status,
            version="0.1.0",
            uptime=time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0
        )
        
    except Exception as e:
        log_error(e, context={"endpoint": "/health"})
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")


@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the current model."""
    try:
        if not predictor:
            raise HTTPException(status_code=503, detail="Model not available")
        
        model_info = predictor.get_model_info()
        return ModelInfoResponse(**model_info)
        
    except Exception as e:
        log_error(e, context={"endpoint": "/model/info"})
        raise HTTPException(status_code=500, detail="Failed to get model info")


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a single prediction."""
    try:
        if not predictor:
            raise HTTPException(status_code=503, detail="Model not available")
        
        # Convert request to dict
        input_data = request.model_dump()
        
        # Make prediction
        result = predictor.predict(input_data)
        
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            model_id=result.get("model_id"),
            processing_time=result.get("processing_time", 0.0)
        )
        
    except ValueError as e:
        # Input validation error
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        log_error(e, context={"endpoint": "/predict"})
        raise HTTPException(status_code=500, detail="Prediction failed")


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Make batch predictions."""
    try:
        if not predictor:
            raise HTTPException(status_code=503, detail="Model not available")
        
        # Convert requests to list of dicts
        input_data = [item.model_dump() for item in request.inputs]
        
        # Make batch predictions
        results = predictor.predict_batch(input_data)
        
        predictions = []
        for result in results:
            predictions.append(PredictionResponse(
                prediction=result["prediction"],
                confidence=result["confidence"],
                model_id=result.get("model_id"),
                processing_time=result.get("processing_time", 0.0)
            ))
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_count=len(predictions),
            processing_time=sum(p.processing_time for p in predictions)
        )
        
    except ValueError as e:
        # Input validation error
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        log_error(e, context={"endpoint": "/predict/batch"})
        raise HTTPException(status_code=500, detail="Batch prediction failed")


# Set startup time
app.state.start_time = time.time()
