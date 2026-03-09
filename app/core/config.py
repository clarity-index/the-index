"""
Configuration management for The Index.

This module provides application configuration using Pydantic settings.
"""

from typing import Optional, List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "The Index"
    app_version: str = "0.1.0"
    debug: bool = False

    # API
    api_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # BitRep Integration (Placeholder)
    bitrep_endpoint: Optional[str] = None
    bitrep_enabled: bool = False

    # Governance
    governance_quorum_threshold: float = 0.5
    governance_quadratic_scaling: bool = True

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
