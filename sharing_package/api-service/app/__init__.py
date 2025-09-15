"""
Income Prediction API Service

A FastAPI-based service that wraps the existing income prediction pipeline
to provide REST API endpoints for real-time and batch predictions.

This service does NOT modify any existing code - it imports and uses
the existing production pipeline from models/production/
"""

__version__ = "1.0.0"
__author__ = "Caja de Ahorros ML Team"
__description__ = "Income Prediction API Service"
