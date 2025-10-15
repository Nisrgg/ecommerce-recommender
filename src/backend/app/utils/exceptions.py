"""
Custom exception classes for the E-commerce Recommender application.

This module defines specific exception types for better error handling
and more informative error messages.
"""

from typing import Optional


class EcommerceRecommenderError(Exception):
    """Base exception for E-commerce Recommender application."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class RecommendationError(EcommerceRecommenderError):
    """Exception raised when recommendation generation fails."""
    pass


class AIExplanationError(EcommerceRecommenderError):
    """Exception raised when AI explanation generation fails."""
    pass


class DatabaseError(EcommerceRecommenderError):
    """Exception raised when database operations fail."""
    pass


class UserNotFoundError(EcommerceRecommenderError):
    """Exception raised when a user is not found."""
    pass


class ProductNotFoundError(EcommerceRecommenderError):
    """Exception raised when a product is not found."""
    pass


class ConfigurationError(EcommerceRecommenderError):
    """Exception raised when configuration is invalid."""
    pass


class CacheError(EcommerceRecommenderError):
    """Exception raised when cache operations fail."""
    pass

