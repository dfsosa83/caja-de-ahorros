"""
Unit tests for configuration management.
"""

import pytest
from pathlib import Path

from income_estimator.config import Config, get_config, load_config


@pytest.mark.unit
class TestConfig:
    """Test configuration management."""
    
    def test_default_config_creation(self):
        """Test creating default configuration."""
        config = Config()
        
        assert config.environment == "development"
        assert config.debug is False
        assert config.data.train_test_split == 0.2
        assert config.model.hyperparameter_tuning is True
        assert config.api.port == 8000
    
    def test_config_from_dict(self):
        """Test creating configuration from dictionary."""
        config_dict = {
            "environment": "test",
            "debug": True,
            "api": {
                "port": 9000,
                "host": "127.0.0.1"
            }
        }
        
        config = Config(**config_dict)
        
        assert config.environment == "test"
        assert config.debug is True
        assert config.api.port == 9000
        assert config.api.host == "127.0.0.1"
    
    def test_get_data_path(self):
        """Test getting data paths."""
        config = Config()
        
        raw_path = config.get_data_path("raw")
        processed_path = config.get_data_path("processed")
        external_path = config.get_data_path("external")
        
        assert isinstance(raw_path, Path)
        assert isinstance(processed_path, Path)
        assert isinstance(external_path, Path)
        
        assert "raw" in str(raw_path)
        assert "processed" in str(processed_path)
        assert "external" in str(external_path)
    
    def test_get_model_path(self):
        """Test getting model path."""
        config = Config()
        model_path = config.get_model_path()
        
        assert isinstance(model_path, Path)
        assert "models" in str(model_path)
    
    def test_get_log_path(self):
        """Test getting log path."""
        config = Config()
        log_path = config.get_log_path()
        
        assert isinstance(log_path, Path)
        assert "logs" in str(log_path)
    
    def test_invalid_data_type(self):
        """Test invalid data type raises error."""
        config = Config()
        
        with pytest.raises(ValueError, match="Unknown data type"):
            config.get_data_path("invalid")
    
    def test_config_to_dict(self):
        """Test converting configuration to dictionary."""
        config = Config()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "environment" in config_dict
        assert "data" in config_dict
        assert "model" in config_dict
        assert "api" in config_dict
    
    def test_get_global_config(self):
        """Test getting global configuration instance."""
        config = get_config()
        
        assert isinstance(config, Config)
        
        # Should return the same instance
        config2 = get_config()
        assert config is config2
