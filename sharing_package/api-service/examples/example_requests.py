"""
Example requests for the Income Prediction API

This script demonstrates how to use the API endpoints with real examples.
Run this script to test the API after starting the service.

Usage:
    python examples/example_requests.py
"""

import requests
import json
import time
from typing import Dict, List


class IncomePredictionAPIClient:
    """Client for interacting with the Income Prediction API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        response = self.session.get(f"{self.base_url}/api/v1/model/info")
        response.raise_for_status()
        return response.json()
    
    def predict_single(self, customer_data: Dict) -> Dict:
        """Make a single prediction"""
        response = self.session.post(
            f"{self.base_url}/api/v1/predict",
            json=customer_data
        )
        response.raise_for_status()
        return response.json()
    
    def predict_batch(self, customers: List[Dict]) -> Dict:
        """Make batch predictions"""
        batch_data = {"customers": customers}
        response = self.session.post(
            f"{self.base_url}/api/v1/predict/batch",
            json=batch_data
        )
        response.raise_for_status()
        return response.json()


def create_sample_customers() -> List[Dict]:
    """Create sample customer data for testing"""
    return [
        {
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
        },
        {
            "cliente": "CUST002",
            "identificador_unico": "ID002",
            "edad": 28,
            "ocupacion": "Contador",
            "fechaingresoempleo": "2021-03-10",
            "nombreempleadorcliente": "Finance Corp",
            "cargoempleocliente": "Junior Accountant",
            "saldo": 2500.0,
            "monto_letra": 150.0,
            "fecha_inicio": "2020-08-15",
            "sexo": "F",
            "ciudad": "Cartago",
            "pais": "Costa Rica",
            "estado_civil": "Soltero"
        },
        {
            "cliente": "CUST003",
            "identificador_unico": "ID003",
            "edad": 42,
            "ocupacion": "Médico",
            "fechaingresoempleo": "2018-06-01",
            "nombreempleadorcliente": "Hospital Nacional",
            "cargoempleocliente": "Especialista",
            "saldo": 8500.0,
            "monto_letra": 400.0,
            "fecha_inicio": "2017-12-01",
            "sexo": "M",
            "ciudad": "Alajuela",
            "pais": "Costa Rica",
            "estado_civil": "Casado"
        }
    ]


def main():
    """Main example execution"""
    print("🏦 Income Prediction API - Example Usage")
    print("=" * 50)
    
    # Initialize client
    client = IncomePredictionAPIClient()
    
    try:
        # 1. Health Check
        print("\n1. 🔍 Health Check")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Model: {health['model_status']}")
        print(f"   Version: {health['version']}")
        print(f"   Uptime: {health['uptime_seconds']:.1f}s")
        
        # 2. Model Information
        print("\n2. 📊 Model Information")
        try:
            model_info = client.get_model_info()
            print(f"   API Version: {model_info['api_version']}")
            print(f"   Max Batch Size: {model_info['max_batch_size']}")
            if 'model_info' in model_info:
                print(f"   Model Loaded: {model_info['model_info']['model_loaded']}")
                print(f"   Features: {model_info['model_info']['feature_count']}")
        except requests.exceptions.HTTPError as e:
            print(f"   ⚠️ Model info unavailable: {e}")
        
        # 3. Single Prediction
        print("\n3. 🎯 Single Customer Prediction")
        sample_customers = create_sample_customers()
        customer = sample_customers[0]
        
        print(f"   Customer: {customer['cliente']}")
        print(f"   Age: {customer['edad']}")
        print(f"   Occupation: {customer['ocupacion']}")
        print(f"   Balance: ${customer['saldo']:,.2f}")
        
        try:
            start_time = time.time()
            prediction = client.predict_single(customer)
            end_time = time.time()
            
            print(f"   ✅ Predicted Income: ${prediction['predicted_income']:,.2f}")
            print(f"   Confidence: {prediction.get('confidence_score', 'N/A')}")
            print(f"   Processing Time: {prediction['processing_time_ms']:.1f}ms")
            print(f"   Total Time: {(end_time - start_time) * 1000:.1f}ms")
            
        except requests.exceptions.HTTPError as e:
            print(f"   ❌ Prediction failed: {e}")
        
        # 4. Batch Prediction
        print("\n4. 📦 Batch Prediction")
        print(f"   Customers: {len(sample_customers)}")
        
        try:
            start_time = time.time()
            batch_result = client.predict_batch(sample_customers)
            end_time = time.time()
            
            predictions = batch_result['predictions']
            summary = batch_result['batch_summary']
            
            print(f"   ✅ Successful: {summary['successful_predictions']}/{summary['total_customers']}")
            print(f"   Average Income: ${summary['average_income']:,.2f}")
            print(f"   Processing Time: {batch_result['total_processing_time_ms']:.1f}ms")
            print(f"   Total Time: {(end_time - start_time) * 1000:.1f}ms")
            
            print("\n   Individual Results:")
            for pred in predictions:
                print(f"   - {pred['customer_id']}: ${pred['predicted_income']:,.2f}")
                
        except requests.exceptions.HTTPError as e:
            print(f"   ❌ Batch prediction failed: {e}")
        
        print("\n✅ All examples completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the API server running?")
        print("   Start the server with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
