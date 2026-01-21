"""
Configuration settings for NewsPulse AI
Loads environment variables and provides application-wide configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    google_api_key: str = ""
    google_search_api_key: str = ""
    google_search_engine_id: str = ""

    # Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    # Application Settings
    log_level: str = "INFO"
    max_articles_per_report: int = 10
    verification_max_retries: int = 2  # Reduced from 3 for faster testing
    report_delivery_time: str = "08:00"

    # Model Configuration
    gemini_model: str = "models/gemini-2.5-flash"  # Latest Gemini model
    temperature: float = 0.7
    max_tokens: int = 8192

    # Data directories
    data_dir: Path = Path(__file__).parent.parent / "data"
    user_profiles_dir: Path = data_dir / "user_profiles"
    history_dir: Path = data_dir / "history"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure data directories exist
        self.user_profiles_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def validate_api_keys(self):
        """Validate that required API keys are set"""
        missing_keys = []
        if not self.google_api_key:
            missing_keys.append("GOOGLE_API_KEY")
        if not self.google_search_api_key:
            missing_keys.append("GOOGLE_SEARCH_API_KEY")
        if not self.google_search_engine_id:
            missing_keys.append("GOOGLE_SEARCH_ENGINE_ID")

        if missing_keys:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_keys)}\n"
                f"Please set them in your .env file"
            )


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Warning: Could not load settings from .env file: {e}")
    print("Please create a .env file with your API keys. See .env.example for reference.")
    settings = None
