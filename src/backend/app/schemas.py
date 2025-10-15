"""
Pydantic schemas for API request/response models.

This module defines all the data models used for API serialization
and validation using Pydantic.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    description: Optional[str] = Field(None, description="Product description")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    product_id: int = Field(..., description="Unique product identifier")


class ProductResponse(ProductBase):
    """Schema for product response."""
    product_id: int = Field(..., description="Unique product identifier")
    
    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    """Base interaction schema."""
    user_id: int = Field(..., description="User identifier")
    product_id: int = Field(..., description="Product identifier")
    event_type: str = Field(..., description="Type of interaction (view, purchase, etc.)")


class InteractionCreate(InteractionBase):
    """Schema for creating a new interaction."""
    pass


class InteractionResponse(InteractionBase):
    """Schema for interaction response."""
    id: int = Field(..., description="Unique interaction identifier")
    timestamp: datetime = Field(..., description="When the interaction occurred")
    
    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    """Schema for a single recommendation with explanation."""
    product: ProductResponse = Field(..., description="Recommended product")
    explanation: str = Field(..., description="AI-generated explanation for the recommendation")


class RecommendationsResponse(BaseModel):
    """Schema for complete recommendations response."""
    source_product: ProductResponse = Field(..., description="Product that triggered the recommendations")
    recommendations: List[RecommendationResponse] = Field(..., description="List of recommendations")
    user_id: int = Field(..., description="User identifier")
    generated_at: datetime = Field(..., description="When recommendations were generated")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str = Field(..., description="Error message")
    detail: str = Field(..., description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the error occurred")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    gemini_available: bool = Field(..., description="Whether Gemini AI service is available")
    version: str = Field(..., description="Application version")


class UserInteractionsResponse(BaseModel):
    """Schema for user interactions response."""
    user_id: int = Field(..., description="User identifier")
    interactions: List[InteractionResponse] = Field(..., description="List of user interactions")


class StatsResponse(BaseModel):
    """Schema for statistics response."""
    total_products: int = Field(..., description="Total number of products")
    total_interactions: int = Field(..., description="Total number of interactions")
    unique_users: int = Field(..., description="Number of unique users")
    unique_products: int = Field(..., description="Number of products with interactions")
    categories: List[str] = Field(..., description="List of product categories")

