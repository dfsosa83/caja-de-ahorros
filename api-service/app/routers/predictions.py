"""
Prediction endpoints for the Income Prediction API
"""

import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    CustomerInput, 
    BatchPredictionInput,
    PredictionResponse, 
    BatchPredictionResponse,
    ErrorResponse
)
from app.services.prediction_service import PredictionService
from app.core.logging import get_logger
from app.core.config import get_settings

logger = get_logger("predictions_router")
settings = get_settings()

# Create router
router = APIRouter(prefix="/api/v1", tags=["predictions"])

# Global prediction service instance
prediction_service = None


def get_prediction_service() -> PredictionService:
    """Dependency to get prediction service instance"""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict income for a single customer",
    description="Make an income prediction for a single customer using the trained ML model"
)
async def predict_single_customer(
    customer: CustomerInput,
    service: PredictionService = Depends(get_prediction_service)
) -> PredictionResponse:
    """
    Predict income for a single customer
    
    - **customer**: Customer data including demographics, employment, and financial information
    - **returns**: Predicted income with confidence score and contributing factors
    """
    try:
        logger.info(f"Received prediction request for customer: {customer.cliente}")
        
        # Validate service health
        if not service.is_healthy():
            raise HTTPException(
                status_code=503,
                detail="Prediction service is not available"
            )
        
        # Make prediction
        prediction = service.predict_single(customer)
        
        logger.info(f"Prediction successful for customer {customer.cliente}: ${prediction.predicted_income:.2f}")
        return prediction
        
    except ValueError as e:
        logger.error(f"Validation error for customer {customer.cliente}: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.error(f"Prediction error for customer {customer.cliente}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    summary="Predict income for multiple customers",
    description="Make income predictions for multiple customers in a single request"
)
async def predict_batch_customers(
    batch_input: BatchPredictionInput,
    background_tasks: BackgroundTasks,
    service: PredictionService = Depends(get_prediction_service)
) -> BatchPredictionResponse:
    """
    Predict income for multiple customers
    
    - **batch_input**: List of customers for batch prediction
    - **returns**: List of predictions with batch summary statistics
    """
    try:
        start_time = time.time()
        customer_count = len(batch_input.customers)
        
        logger.info(f"Received batch prediction request for {customer_count} customers")
        
        # Validate service health
        if not service.is_healthy():
            raise HTTPException(
                status_code=503,
                detail="Prediction service is not available"
            )
        
        # Validate batch size
        if customer_count > settings.max_batch_size:
            raise HTTPException(
                status_code=422,
                detail=f"Batch size {customer_count} exceeds maximum allowed {settings.max_batch_size}"
            )
        
        # Make batch predictions
        predictions, batch_summary = service.predict_batch(batch_input.customers)
        
        # Calculate total processing time
        total_time_ms = (time.time() - start_time) * 1000
        
        # Create response
        response = BatchPredictionResponse(
            predictions=predictions,
            batch_summary=batch_summary,
            total_processing_time_ms=total_time_ms
        )
        
        logger.info(f"Batch prediction completed: {len(predictions)}/{customer_count} successful")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error in batch prediction: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/model/info",
    summary="Get model information",
    description="Get information about the loaded model and its capabilities"
)
async def get_model_info(
    service: PredictionService = Depends(get_prediction_service)
) -> dict:
    """
    Get model information and status
    
    - **returns**: Model metadata including version, features, and status
    """
    try:
        model_info = service.get_model_info()
        return {
            "model_info": model_info,
            "api_version": settings.app_version,
            "max_batch_size": settings.max_batch_size,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )
