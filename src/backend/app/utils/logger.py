"""
Centralized logging configuration.

This module provides a standardized logging setup for the entire application
with proper formatting, levels, and handlers.
"""

import logging
import sys
from typing import Optional

from app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up application logging with proper configuration.
    
    Args:
        log_level: Optional log level override
        
    Returns:
        Configured logger instance
    """
    level = log_level or settings.log_level
    
    # Create logger
    logger = logging.getLogger("ecommerce_recommender")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create formatter
    formatter = logging.Formatter(settings.log_format)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"ecommerce_recommender.{name}")


# Initialize main logger
main_logger = setup_logging()

