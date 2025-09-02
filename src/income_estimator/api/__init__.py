"""
API module for the Income Estimator ML project.
"""

from .app import app
from .models import PredictionRequest, PredictionResponse

__all__ = ["app", "PredictionRequest", "PredictionResponse"]
