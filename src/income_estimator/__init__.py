"""
Income Estimator ML Package

A production-ready machine learning project for income estimation using modern MLOps practices.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import Config
from .logger import get_logger

__all__ = ["Config", "get_logger", "__version__"]
