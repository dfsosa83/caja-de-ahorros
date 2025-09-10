"""
API endpoint tests for the Income Estimator ML project.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.api
class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint returns 200."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "model_status" in data
        assert "version" in data
        assert "uptime" in data


@pytest.mark.api
class TestMetricsEndpoint:
    """Test metrics endpoint."""
    
    def test_metrics_endpoint(self, client: TestClient):
        """Test metrics endpoint returns prometheus format."""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"


@pytest.mark.api
class TestPredictionEndpoints:
    """Test prediction endpoints."""
    
    def test_predict_endpoint_structure(self, client: TestClient, sample_prediction_data):
        """Test prediction endpoint structure (may fail without model)."""
        response = client.post("/predict", json=sample_prediction_data)
        
        # May return 503 if no model is loaded, which is expected
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "confidence" in data
            assert "processing_time" in data
    
    def test_predict_invalid_data(self, client: TestClient):
        """Test prediction with invalid data."""
        invalid_data = {
            "age": -5,  # Invalid age
            "education_num": 25,  # Invalid education years
        }
        
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_batch_predict_endpoint_structure(self, client: TestClient, sample_batch_data):
        """Test batch prediction endpoint structure."""
        response = client.post("/predict/batch", json=sample_batch_data)
        
        # May return 503 if no model is loaded, which is expected
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert "total_count" in data
            assert "processing_time" in data


@pytest.mark.api
class TestModelInfoEndpoint:
    """Test model info endpoint."""
    
    def test_model_info_endpoint(self, client: TestClient):
        """Test model info endpoint."""
        response = client.get("/model/info")
        
        # May return 503 if no model is loaded, which is expected
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "model_id" in data
            assert "algorithm" in data
            assert "accuracy" in data
            assert "features" in data


@pytest.mark.api
class TestAPIDocumentation:
    """Test API documentation endpoints."""
    
    def test_openapi_schema(self, client: TestClient):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint(self, client: TestClient):
        """Test Swagger UI docs endpoint."""
        response = client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self, client: TestClient):
        """Test ReDoc docs endpoint."""
        response = client.get("/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
