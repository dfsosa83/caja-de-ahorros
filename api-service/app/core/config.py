"""
Configuration settings for the Income Prediction API Service
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "Income Prediction API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model Configuration
    model_path: str = "../../models/production/final_production_model_nested_cv.pkl"
    pipeline_module: str = "models.production.00_predictions_pipeline"
    
    # Data Configuration
    max_batch_size: int = 1000
    prediction_timeout: int = 30  # seconds
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Configuration
    api_key_header: str = "X-API-Key"
    cors_origins: list = ["*"]  # Configure appropriately for production
    
    # Health Check Configuration
    health_check_timeout: int = 5
    
    class Config:
        env_file = ".env"
        env_prefix = "API_"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
