"""
Pydantic models for API request/response validation.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PredictionRequest(BaseModel):
    """Request model for single prediction."""
    
    # Numerical features
    age: int = Field(..., ge=16, le=100, description="Age of the person")
    education_num: int = Field(..., ge=1, le=16, description="Number of years of education")
    hours_per_week: int = Field(..., ge=1, le=100, description="Hours worked per week")
    capital_gain: int = Field(..., ge=0, description="Capital gains")
    capital_loss: int = Field(..., ge=0, description="Capital losses")
    
    # Categorical features
    education: str = Field(..., description="Education level")
    occupation: str = Field(..., description="Occupation")
    marital_status: str = Field(..., description="Marital status")
    relationship: str = Field(..., description="Relationship status")
    race: str = Field(..., description="Race")
    sex: str = Field(..., description="Gender")
    native_country: str = Field(..., description="Native country")
    
    @validator('sex')
    def validate_sex(cls, v):
        """Validate sex field."""
        allowed_values = ['Male', 'Female']
        if v not in allowed_values:
            raise ValueError(f"Sex must be one of: {allowed_values}")
        return v
    
    @validator('education')
    def validate_education(cls, v):
        """Validate education field."""
        allowed_values = [
            'Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school',
            'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters',
            '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'
        ]
        if v not in allowed_values:
            raise ValueError(f"Education must be one of: {allowed_values}")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "education_num": 13,
                "hours_per_week": 40,
                "capital_gain": 0,
                "capital_loss": 0,
                "education": "Bachelors",
                "occupation": "Tech-support",
                "marital_status": "Married-civ-spouse",
                "relationship": "Husband",
                "race": "White",
                "sex": "Male",
                "native_country": "United-States"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for single prediction."""
    
    prediction: str = Field(..., description="Predicted income class (<=50K or >50K)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence score")
    model_id: Optional[str] = Field(None, description="ID of the model used for prediction")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction": ">50K",
                "confidence": 0.85,
                "model_id": "random_forest_20240101_120000",
                "processing_time": 0.023
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions."""
    
    inputs: List[PredictionRequest] = Field(..., description="List of prediction inputs")
    
    @validator('inputs')
    def validate_inputs_length(cls, v):
        """Validate batch size."""
        if len(v) == 0:
            raise ValueError("At least one input is required")
        if len(v) > 1000:
            raise ValueError("Maximum batch size is 1000")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "age": 35,
                        "education_num": 13,
                        "hours_per_week": 40,
                        "capital_gain": 0,
                        "capital_loss": 0,
                        "education": "Bachelors",
                        "occupation": "Tech-support",
                        "marital_status": "Married-civ-spouse",
                        "relationship": "Husband",
                        "race": "White",
                        "sex": "Male",
                        "native_country": "United-States"
                    },
                    {
                        "age": 28,
                        "education_num": 12,
                        "hours_per_week": 35,
                        "capital_gain": 0,
                        "capital_loss": 0,
                        "education": "HS-grad",
                        "occupation": "Sales",
                        "marital_status": "Never-married",
                        "relationship": "Not-in-family",
                        "race": "Black",
                        "sex": "Female",
                        "native_country": "United-States"
                    }
                ]
            }
        }


class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    
    predictions: List[PredictionResponse] = Field(..., description="List of prediction results")
    total_count: int = Field(..., description="Total number of predictions")
    processing_time: float = Field(..., ge=0.0, description="Total processing time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "prediction": ">50K",
                        "confidence": 0.85,
                        "model_id": "random_forest_20240101_120000",
                        "processing_time": 0.023
                    },
                    {
                        "prediction": "<=50K",
                        "confidence": 0.72,
                        "model_id": "random_forest_20240101_120000",
                        "processing_time": 0.019
                    }
                ],
                "total_count": 2,
                "processing_time": 0.042
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Overall service status")
    model_status: str = Field(..., description="Model availability status")
    version: str = Field(..., description="API version")
    uptime: float = Field(..., ge=0.0, description="Service uptime in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "model_status": "healthy",
                "version": "0.1.0",
                "uptime": 3600.5
            }
        }


class ModelInfoResponse(BaseModel):
    """Response model for model information."""
    
    model_id: str = Field(..., description="Model identifier")
    algorithm: str = Field(..., description="Algorithm used")
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Model accuracy")
    f1_score: float = Field(..., ge=0.0, le=1.0, description="Model F1 score")
    created_at: str = Field(..., description="Model creation timestamp")
    features: List[str] = Field(..., description="List of input features")
    target_classes: List[str] = Field(..., description="List of target classes")
    
    class Config:
        schema_extra = {
            "example": {
                "model_id": "random_forest_20240101_120000",
                "algorithm": "random_forest",
                "accuracy": 0.8542,
                "f1_score": 0.7891,
                "created_at": "2024-01-01T12:00:00Z",
                "features": [
                    "age", "education_num", "hours_per_week", "capital_gain",
                    "capital_loss", "education", "occupation", "marital_status",
                    "relationship", "race", "sex", "native_country"
                ],
                "target_classes": ["<=50K", ">50K"]
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: Optional[str] = Field(None, description="Error timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Model not available",
                "error_code": "MODEL_UNAVAILABLE",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
