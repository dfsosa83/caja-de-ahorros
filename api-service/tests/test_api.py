"""
Test suite for the Income Prediction API
"""

import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "model_status" in data
        assert "version" in data
        assert "uptime_seconds" in data
    
    def test_detailed_health_check(self):
        """Test detailed health check"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        
        data = response.json()
        assert "service" in data
        assert "model" in data
        assert "system" in data
        assert "timestamp" in data
    
    def test_readiness_check(self):
        """Test readiness check"""
        response = client.get("/ready")
        # May be 200 or 503 depending on model loading
        assert response.status_code in [200, 503]
    
    def test_liveness_check(self):
        """Test liveness check"""
        response = client.get("/live")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "alive"


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test API root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "Income Prediction API"
        assert "version" in data
        assert "endpoints" in data


class TestPredictionEndpoints:
    """Test prediction endpoints"""
    
    @pytest.fixture
    def sample_customer(self):
        """Sample customer data for testing"""
        return {
            "cliente": "TEST001",
            "identificador_unico": "TEST_ID_001",
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
    
    def test_model_info(self):
        """Test model info endpoint"""
        response = client.get("/api/v1/model/info")
        # May be 200 or 500 depending on model loading
        assert response.status_code in [200, 500]
    
    def test_single_prediction_validation(self):
        """Test input validation for single prediction"""
        # Test with invalid data
        invalid_customer = {
            "cliente": "TEST001",
            "edad": 150,  # Invalid age
            "ocupacion": "Ingeniero"
            # Missing required fields
        }
        
        response = client.post("/api/v1/predict", json=invalid_customer)
        assert response.status_code == 422  # Validation error
    
    def test_batch_prediction_validation(self):
        """Test input validation for batch prediction"""
        # Test with empty batch
        empty_batch = {"customers": []}
        
        response = client.post("/api/v1/predict/batch", json=empty_batch)
        assert response.status_code == 422  # Validation error
    
    def test_batch_size_limit(self):
        """Test batch size limit"""
        # Create a batch that exceeds the limit
        large_batch = {
            "customers": [
                {
                    "cliente": f"TEST{i:04d}",
                    "edad": 30,
                    "ocupacion": "Test",
                    "fechaingresoempleo": "2020-01-01",
                    "nombreempleadorcliente": "Test Company",
                    "cargoempleocliente": "Test Position",
                    "saldo": 1000.0,
                    "fecha_inicio": "2019-01-01"
                }
                for i in range(1001)  # Exceeds max batch size
            ]
        }
        
        response = client.post("/api/v1/predict/batch", json=large_batch)
        assert response.status_code == 422  # Validation error


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_endpoint(self):
        """Test non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_json(self):
        """Test invalid JSON in request"""
        response = client.post(
            "/api/v1/predict",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_content_type(self):
        """Test missing content type"""
        response = client.post("/api/v1/predict", data='{"test": "data"}')
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
