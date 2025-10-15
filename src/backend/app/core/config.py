"""
Configuration management using Pydantic Settings.

This module handles all environment variables and application configuration
with proper validation and type checking.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = Field(default="E-commerce Product Recommender", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./ecommerce.db", env="DATABASE_URL")
    
    # AI Configuration
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-pro", env="GEMINI_MODEL")
    
    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
        env="CORS_ORIGINS"
    )
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Cache Configuration
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    enable_cache: bool = Field(default=True, env="ENABLE_CACHE")
    
    # Recommendation Configuration
    default_recommendations: int = Field(default=3, env="DEFAULT_RECOMMENDATIONS")
    max_recommendations: int = Field(default=10, env="MAX_RECOMMENDATIONS")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()

