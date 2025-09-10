"""
Logging utilities for the Income Estimator ML project.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger

from .config import get_config


class JSONFormatter:
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: Dict[str, Any]) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "logger": record["name"],
            "module": record["module"],
            "function": record["function"],
            "line": record["line"],
            "message": record["message"],
        }
        
        # Add extra fields if present
        if "extra" in record:
            log_entry.update(record["extra"])
        
        return json.dumps(log_entry)


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_json: Optional[bool] = None,
    rotation: Optional[str] = None,
    retention: Optional[str] = None,
) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        enable_json: Whether to use JSON formatting
        rotation: Log rotation policy
        retention: Log retention policy
    """
    config = get_config()
    
    # Use provided values or fall back to config
    log_level = log_level or config.logging.level
    log_file = log_file or str(config.get_log_path())
    enable_json = enable_json if enable_json is not None else config.logging.enable_json_logs
    rotation = rotation or config.logging.rotation
    retention = retention or config.logging.retention
    
    # Remove default handler
    logger.remove()
    
    # Console handler
    if enable_json:
        logger.add(
            sys.stdout,
            level=log_level,
            format=JSONFormatter().format,
            colorize=False,
        )
    else:
        logger.add(
            sys.stdout,
            level=log_level,
            format=config.logging.format,
            colorize=True,
        )
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if enable_json:
            logger.add(
                log_file,
                level=log_level,
                format=JSONFormatter().format,
                rotation=rotation,
                retention=retention,
                compression="gz",
            )
        else:
            logger.add(
                log_file,
                level=log_level,
                format=config.logging.format,
                rotation=rotation,
                retention=retention,
                compression="gz",
            )


def get_logger(name: str) -> Any:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


def log_function_call(func_name: str, **kwargs: Any) -> None:
    """
    Log function call with parameters.
    
    Args:
        func_name: Name of the function being called
        **kwargs: Function parameters to log
    """
    logger.info(
        f"Calling function: {func_name}",
        extra={"function_call": func_name, "parameters": kwargs}
    )


def log_model_metrics(model_name: str, metrics: Dict[str, float]) -> None:
    """
    Log model performance metrics.
    
    Args:
        model_name: Name of the model
        metrics: Dictionary of metric names and values
    """
    logger.info(
        f"Model metrics for {model_name}",
        extra={"model_name": model_name, "metrics": metrics}
    )


def log_api_request(
    method: str,
    endpoint: str,
    status_code: int,
    response_time: float,
    user_id: Optional[str] = None,
) -> None:
    """
    Log API request details.
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        status_code: HTTP status code
        response_time: Response time in seconds
        user_id: Optional user identifier
    """
    logger.info(
        f"{method} {endpoint} - {status_code}",
        extra={
            "api_request": {
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time": response_time,
                "user_id": user_id,
            }
        }
    )


def log_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None,
) -> None:
    """
    Log error with context information.
    
    Args:
        error: Exception that occurred
        context: Additional context information
        user_id: Optional user identifier
    """
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "user_id": user_id,
    }
    
    if context:
        error_info["context"] = context
    
    logger.error(
        f"Error occurred: {error}",
        extra={"error": error_info}
    )


# Initialize logging on module import
setup_logging()
