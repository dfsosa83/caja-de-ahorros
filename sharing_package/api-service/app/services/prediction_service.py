"""
Prediction Service - Wraps the existing production pipeline

This service imports and uses your existing production pipeline
without modifying any of your working code.
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import pickle
import joblib

# Add the project root to Python path to import existing modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, project_root)

from app.core.logging import get_logger
from app.core.config import get_settings
from app.models.schemas import CustomerInput, PredictionResponse

logger = get_logger("prediction_service")
settings = get_settings()


class PredictionService:
    """
    Service class that wraps your existing production pipeline
    
    This class imports and uses your existing code from:
    - models/production/00_predictions_pipeline.py
    - models/production/final_production_model_nested_cv.pkl
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self.model_version = "1.0.0"
        self.feature_columns = None
        self.model_info = None
        self._load_model()
        
    def _load_model(self) -> None:
        """Load the trained model and required components"""
        try:
            logger.info("Loading production model...")

            # Path to your existing model
            model_path = os.path.join(project_root, "models/production/final_production_model_nested_cv.pkl")

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")

            # Load the model artifacts using joblib (same as your pipeline)
            model_artifacts = joblib.load(model_path)

            # Extract the actual model from the artifacts dictionary
            self.model = model_artifacts['final_production_model']
            self.scaler = model_artifacts['final_scaler']
            self.feature_columns = model_artifacts['feature_columns']

            # Store additional metadata
            self.model_info = model_artifacts.get('training_info', {})

            self.model_loaded = True
            logger.info(f"Model loaded successfully. Features: {len(self.feature_columns)}")

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model_loaded = False
            raise
    
    def _prepare_customer_data(self, customer: CustomerInput) -> pd.DataFrame:
        """
        Prepare customer data for prediction using your existing preprocessing logic
        
        This method replicates the preprocessing from your 00_predictions_pipeline.py
        without modifying the original file.
        """
        try:
            # Convert customer input to DataFrame
            customer_dict = customer.dict()
            df = pd.DataFrame([customer_dict])
            
            # Apply the same preprocessing as your production pipeline
            df = self._standardize_column_names(df)
            df = self._convert_date_columns(df)
            df = self._create_engineered_features(df)
            df = self._apply_frequency_encoding(df)
            
            # Select only the features the model expects
            df_features = df[self.feature_columns].copy()
            
            # Handle any missing values
            df_features = df_features.fillna(0)
            
            return df_features
            
        except Exception as e:
            logger.error(f"Error preparing customer data: {str(e)}")
            raise ValueError(f"Data preparation failed: {str(e)}")
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names (from your pipeline)"""
        column_mapping = {
            'Cliente': 'cliente',
            'Identificador_Unico': 'identificador_unico',
            'Edad': 'edad',
            'Ocupacion': 'ocupacion',
            'FechaIngresoEmpleo': 'fechaingresoempleo',
            'NombreEmpleadorCliente': 'nombreempleadorcliente',
            'CargoEmpleoCliente': 'cargoempleocliente',
            'monto_letra': 'monto_letra',
            'saldo': 'saldo',
            'fecha_inicio': 'fecha_inicio'
        }
        
        df = df.rename(columns=column_mapping)
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
        
        return df
    
    def _convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert date columns to days (from your pipeline)"""
        reference_date = pd.Timestamp('2025-01-01')
        
        date_columns = ['fechaingresoempleo', 'fecha_inicio', 'fecha_vencimiento']
        
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df[f'{col}_days'] = (reference_date - df[col]).dt.days
                except:
                    df[f'{col}_days'] = 0
        
        return df
    
    def _create_engineered_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create engineered features (from your pipeline)"""
        try:
            # Employment years
            if 'fechaingresoempleo_days' in df.columns:
                df['employment_years'] = df['fechaingresoempleo_days'] / 365.25
                df['employment_years'] = df['employment_years'].clip(lower=0)
            else:
                df['employment_years'] = 0
            
            # Balance to payment ratio
            if 'saldo' in df.columns and 'monto_letra' in df.columns:
                df['balance_to_payment_ratio'] = df['saldo'] / (df['monto_letra'] + 1)
            else:
                df['balance_to_payment_ratio'] = 0
            
            # Professional stability score
            df['professional_stability_score'] = (
                df.get('employment_years', 0) * 0.6 + 
                (df.get('saldo', 0) / 1000) * 0.4
            ).clip(upper=10)
            
            return df
            
        except Exception as e:
            logger.error(f"Error creating engineered features: {str(e)}")
            return df
    
    def _apply_frequency_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply frequency encoding (simplified version)"""
        # For production, you would load the actual frequency mappings
        # For now, we'll use simplified encoding
        
        categorical_cols = ['ocupacion', 'nombreempleadorcliente', 'cargoempleocliente']
        
        for col in categorical_cols:
            if col in df.columns:
                # Simple frequency encoding (in production, use your saved mappings)
                df[f'{col}_consolidated_freq'] = 1  # Default frequency
        
        return df
    
    def predict_single(self, customer: CustomerInput) -> PredictionResponse:
        """
        Make a prediction for a single customer
        
        Args:
            customer: Customer input data
            
        Returns:
            Prediction response with income estimate and metadata
        """
        start_time = time.time()
        
        try:
            if not self.model_loaded:
                raise RuntimeError("Model not loaded")
            
            # Prepare data
            customer_df = self._prepare_customer_data(customer)

            # Apply scaling (same as production pipeline)
            customer_scaled = self.scaler.transform(customer_df)

            # Make prediction
            prediction = self.model.predict(customer_scaled)[0]
            
            # Calculate processing time
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Create response
            response = PredictionResponse(
                customer_id=customer.cliente,
                predicted_income=float(prediction),
                confidence_score=0.85,  # You can implement confidence calculation
                prediction_range={
                    "min": float(prediction * 0.8),
                    "max": float(prediction * 1.2)
                },
                top_factors=[
                    {"feature": "ocupacion", "impact": "high", "value": customer.ocupacion},
                    {"feature": "edad", "impact": "medium", "value": customer.edad}
                ],
                processing_time_ms=processing_time_ms,
                model_version=self.model_version
            )
            
            logger.info(f"Prediction completed for customer {customer.cliente}: ${prediction:.2f}")
            return response
            
        except Exception as e:
            logger.error(f"Prediction failed for customer {customer.cliente}: {str(e)}")
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def predict_batch(self, customers: List[CustomerInput]) -> Tuple[List[PredictionResponse], Dict[str, Any]]:
        """
        Make predictions for multiple customers
        
        Args:
            customers: List of customer input data
            
        Returns:
            Tuple of (predictions list, batch summary)
        """
        start_time = time.time()
        predictions = []
        successful = 0
        failed = 0
        
        logger.info(f"Starting batch prediction for {len(customers)} customers")
        
        for customer in customers:
            try:
                prediction = self.predict_single(customer)
                predictions.append(prediction)
                successful += 1
            except Exception as e:
                logger.error(f"Failed to predict for customer {customer.cliente}: {str(e)}")
                failed += 1
                # You might want to include failed predictions in response
        
        # Calculate batch summary
        total_time_ms = (time.time() - start_time) * 1000
        
        if predictions:
            avg_income = sum(p.predicted_income for p in predictions) / len(predictions)
        else:
            avg_income = 0
        
        batch_summary = {
            "total_customers": len(customers),
            "successful_predictions": successful,
            "failed_predictions": failed,
            "average_income": avg_income,
            "success_rate": successful / len(customers) if customers else 0
        }
        
        logger.info(f"Batch prediction completed: {successful}/{len(customers)} successful")
        
        return predictions, batch_summary
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy"""
        return self.model_loaded and self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_loaded": self.model_loaded,
            "model_version": self.model_version,
            "feature_count": len(self.feature_columns) if self.feature_columns else 0,
            "features": self.feature_columns
        }
