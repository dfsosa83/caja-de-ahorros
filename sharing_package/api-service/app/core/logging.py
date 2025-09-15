"""
Logging configuration for the Income Prediction API Service
"""

import logging
import sys
from typing import Optional
from .config import get_settings

settings = get_settings()


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Setup application logging
    
    Args:
        log_level: Optional log level override
        
    Returns:
        Configured logger instance
    """
    level = log_level or settings.log_level
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create application logger
    logger = logging.getLogger("income_prediction_api")
    logger.setLevel(getattr(logging, level.upper()))
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module"""
    return logging.getLogger(f"income_prediction_api.{name}")


# Global logger instance
logger = setup_logging()
