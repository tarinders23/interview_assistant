"""Configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Gemini Configuration
    gemini_api_key: Optional[str] = None  # Optional since we'll get it from the request
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
