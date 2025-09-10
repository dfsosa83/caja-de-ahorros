"""
Configuration management for the Income Estimator ML project.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class DataConfig(BaseModel):
    """Data configuration settings."""
    
    raw_data_path: str = "data/raw"
    processed_data_path: str = "data/processed"
    external_data_path: str = "data/external"
    train_test_split: float = Field(default=0.2, ge=0.1, le=0.5)
    random_state: int = 42
    validation_split: float = Field(default=0.2, ge=0.1, le=0.5)


class ModelConfig(BaseModel):
    """Model configuration settings."""
    
    algorithms: List[str] = [
        "random_forest",
        "gradient_boosting",
        "logistic_regression",
        "svm",
        "neural_network"
    ]
    hyperparameter_tuning: bool = True
    tuning_method: str = "optuna"  # optuna, grid_search, random_search
    n_trials: int = 100
    cv_folds: int = 5
    scoring_metric: str = "accuracy"
    model_registry_path: str = "models"
    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "income_estimator"


class APIConfig(BaseModel):
    """API configuration settings."""
    
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 1
    log_level: str = "info"
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds


class LoggingConfig(BaseModel):
    """Logging configuration settings."""
    
    level: str = "INFO"
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    rotation: str = "1 day"
    retention: str = "30 days"
    log_file: str = "logs/app.log"
    enable_json_logs: bool = False


class MonitoringConfig(BaseModel):
    """Monitoring configuration settings."""
    
    enable_metrics: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 30  # seconds
    model_drift_threshold: float = 0.1
    data_drift_threshold: float = 0.1


class Config(BaseSettings):
    """Main configuration class."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    
    # Sub-configurations
    data: DataConfig = Field(default_factory=DataConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = False
    
    @classmethod
    def from_yaml(cls, config_path: str) -> "Config":
        """Load configuration from YAML file."""
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()
    
    def get_data_path(self, data_type: str = "raw") -> Path:
        """Get absolute path for data directory."""
        if data_type == "raw":
            return self.project_root / self.data.raw_data_path
        elif data_type == "processed":
            return self.project_root / self.data.processed_data_path
        elif data_type == "external":
            return self.project_root / self.data.external_data_path
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    def get_model_path(self) -> Path:
        """Get absolute path for model directory."""
        return self.project_root / self.model.model_registry_path
    
    def get_log_path(self) -> Path:
        """Get absolute path for log file."""
        log_path = self.project_root / self.logging.log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return log_path


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or environment."""
    global config
    
    if config_path and os.path.exists(config_path):
        config = Config.from_yaml(config_path)
    else:
        config = Config()
    
    return config
