"""
Pydantic models for API request and response schemas
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, validator


class CustomerInput(BaseModel):
    """Input schema for a single customer prediction"""
    
    # Required fields based on your production pipeline
    cliente: str = Field(..., description="Customer ID")
    identificador_unico: Optional[str] = Field(None, description="Unique identifier")
    edad: int = Field(..., ge=18, le=100, description="Customer age")
    ocupacion: str = Field(..., description="Customer occupation")
    fechaingresoempleo: str = Field(..., description="Employment start date (YYYY-MM-DD)")
    nombreempleadorcliente: str = Field(..., description="Employer name")
    cargoempleocliente: str = Field(..., description="Job position")
    saldo: float = Field(..., ge=0, description="Account balance")
    monto_letra: Optional[float] = Field(None, ge=0, description="Monthly payment amount")
    fecha_inicio: str = Field(..., description="Account start date (YYYY-MM-DD)")
    
    # Optional fields
    sexo: Optional[str] = Field(None, description="Gender")
    ciudad: Optional[str] = Field(None, description="City")
    pais: Optional[str] = Field(None, description="Country")
    estado_civil: Optional[str] = Field(None, description="Marital status")
    productos_activos: Optional[int] = Field(None, ge=0, description="Active products count")
    letras_mensuales: Optional[int] = Field(None, ge=0, description="Monthly letters count")
    fecha_vencimiento: Optional[str] = Field(None, description="Expiration date (YYYY-MM-DD)")
    monto_prestamo: Optional[float] = Field(None, ge=0, description="Loan amount")
    tasa_prestamo: Optional[float] = Field(None, ge=0, le=100, description="Loan interest rate")
    
    @validator('fechaingresoempleo', 'fecha_inicio', 'fecha_vencimiento')
    def validate_date_format(cls, v):
        """Validate date format"""
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    class Config:
        schema_extra = {
            "example": {
                "cliente": "CUST001",
                "identificador_unico": "ID001",
                "edad": 35,
                "ocupacion": "Ingeniero",
                "fechaingresoempleo": "2020-01-15",
                "nombreempleadorcliente": "Tech Company SA",
                "cargoempleocliente": "Senior Engineer",
                "saldo": 5000.0,
                "monto_letra": 250.0,
                "fecha_inicio": "2019-06-01",
                "sexo": "M",
                "ciudad": "San José",
                "pais": "Costa Rica",
                "estado_civil": "Casado"
            }
        }


class BatchPredictionInput(BaseModel):
    """Input schema for batch predictions"""
    
    customers: List[CustomerInput] = Field(..., description="List of customers for prediction")
    
    @validator('customers')
    def validate_batch_size(cls, v):
        """Validate batch size"""
        if len(v) > 1000:  # Max batch size
            raise ValueError('Batch size cannot exceed 1000 customers')
        if len(v) == 0:
            raise ValueError('Batch cannot be empty')
        return v


class PredictionResponse(BaseModel):
    """Response schema for a single prediction"""
    
    customer_id: str = Field(..., description="Customer ID")
    predicted_income: float = Field(..., description="Predicted income in USD")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="Prediction confidence (0-1)")
    prediction_range: Optional[Dict[str, float]] = Field(None, description="Prediction range (min/max)")
    top_factors: Optional[List[Dict[str, Any]]] = Field(None, description="Top factors influencing prediction")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")
    model_version: str = Field(default="1.0.0", description="Model version used")
    
    class Config:
        schema_extra = {
            "example": {
                "customer_id": "CUST001",
                "predicted_income": 1450.75,
                "confidence_score": 0.85,
                "prediction_range": {
                    "min": 1200.50,
                    "max": 1700.00
                },
                "top_factors": [
                    {"feature": "ocupacion", "impact": "high", "value": "Ingeniero"},
                    {"feature": "edad", "impact": "medium", "value": 35}
                ],
                "processing_time_ms": 45.2,
                "timestamp": "2025-09-10T15:30:00Z",
                "model_version": "1.0.0"
            }
        }


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions"""
    
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    batch_summary: Dict[str, Any] = Field(..., description="Batch processing summary")
    total_processing_time_ms: float = Field(..., description="Total batch processing time")
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "customer_id": "CUST001",
                        "predicted_income": 1450.75,
                        "processing_time_ms": 45.2,
                        "timestamp": "2025-09-10T15:30:00Z"
                    }
                ],
                "batch_summary": {
                    "total_customers": 1,
                    "successful_predictions": 1,
                    "failed_predictions": 0,
                    "average_income": 1450.75
                },
                "total_processing_time_ms": 45.2
            }
        }


class HealthResponse(BaseModel):
    """Health check response schema"""
    
    status: str = Field(..., description="Service status")
    model_status: str = Field(..., description="Model status")
    version: str = Field(..., description="API version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "model_status": "loaded",
                "version": "1.0.0",
                "uptime_seconds": 3600.5,
                "timestamp": "2025-09-10T15:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema"""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {
                    "field": "edad",
                    "issue": "Age must be between 18 and 100"
                },
                "timestamp": "2025-09-10T15:30:00Z"
            }
        }
