import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application settings
    app_name: str = Field("YouTube WebSub Pipeline", description="The name of the application")
    app_version: str = Field("0.0.1", description="The version of the application")
    debug: bool = Field(False, description="Enable or disable debug mode")

    # API configuration
    api_host: str = Field("0.0.0.0", description="API host address")
    api_port: int = Field(8000, description="API port number")
    api_reload: bool = Field(True, description="Enable or disable API auto-reload")

    # Google gemini Configuration
    google_gemini_api_key: str | None = Field(None, description="Google Gemini API key")
    google_gemini_model: str = Field("gemini-2.0-pro", description="Google Gemini model to use")

    # Storage paths
    logs_directory: str = Field("./logs", description="Directory for application logs")

    # Queue Clients
    queue_provider: str = Field("sqs", description="Queue provider to use (e.g., 'sqs')")

    # AWS SQS
    aws_region: str = Field("us-east-1", description="AWS region")
    sqs_queue_url: str = Field(..., description="AWS SQS queue URL")
    aws_access_key_id: str = Field(..., description="AWS access key ID")
    aws_secret_access_key: str = Field(..., description="AWS secret access key")

    # MongoDB configuration
    mongodb_uri: str = Field(
        "mongodb://mongodb:27017", description="MongoDB connection URI"
    )  # Use the service name
    mongodb_db_name: str = Field("youtube_websub", description="MongoDB database name")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings instance."""
    return Settings()


def ensure_directories() -> None:
    """Ensure directories exists."""
    settings = get_settings()
    os.makedirs(settings.logs_directory, exist_ok=True)


ensure_directories()
