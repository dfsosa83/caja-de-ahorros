"""
Pytest configuration and fixtures for the Income Estimator ML project.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from income_estimator.config import Config
from income_estimator.api.app import app


@pytest.fixture(scope="session")
def test_config() -> Config:
    """Create a test configuration."""
    config = Config(
        environment="test",
        debug=True,
        data=Config.DataConfig(
            raw_data_path="tests/data/raw",
            processed_data_path="tests/data/processed",
            external_data_path="tests/data/external",
        ),
        model=Config.ModelConfig(
            model_registry_path="tests/models",
            hyperparameter_tuning=False,
            n_trials=5,
        ),
        logging=Config.LoggingConfig(
            level="DEBUG",
            log_file="tests/logs/test.log",
        ),
    )
    return config


@pytest.fixture(scope="session")
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(scope="function")
def sample_prediction_data() -> dict:
    """Sample data for prediction tests."""
    return {
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


@pytest.fixture(scope="function")
def sample_batch_data(sample_prediction_data) -> dict:
    """Sample batch data for prediction tests."""
    return {
        "inputs": [
            sample_prediction_data,
            {
                **sample_prediction_data,
                "age": 28,
                "education": "HS-grad",
                "sex": "Female",
            }
        ]
    }


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment."""
    # Create test directories
    test_dirs = [
        "tests/data/raw",
        "tests/data/processed", 
        "tests/data/external",
        "tests/models",
        "tests/logs"
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Set test environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"
    
    yield
    
    # Cleanup after tests
    # Note: Temporary directories will be cleaned up automatically


@pytest.fixture(scope="function")
def mock_model_data():
    """Mock model data for testing."""
    return {
        "model_id": "test_model_123",
        "algorithm": "random_forest",
        "accuracy": 0.85,
        "f1_score": 0.82,
        "created_at": "2024-01-01T12:00:00Z",
        "features": [
            "age", "education_num", "hours_per_week", "capital_gain",
            "capital_loss", "education", "occupation", "marital_status",
            "relationship", "race", "sex", "native_country"
        ],
        "target_classes": ["<=50K", ">50K"]
    }


# Pytest markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
