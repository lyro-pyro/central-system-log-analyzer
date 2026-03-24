"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings loaded from environment variables."""

    APP_NAME: str = "AI Secure Data Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Hugging Face configuration
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"
    HUGGINGFACE_TIMEOUT: int = 60

    # File upload limits
    MAX_CONTENT_LENGTH: int = 10_000_000  # characters
    MAX_FILE_SIZE_MB: int = 50  # max file size in MB

    # Log analysis
    LOG_CHUNK_SIZE: int = 5000  # lines per chunk
    MAX_LOG_LINES: int = 1_000_000

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW: int = 60  # seconds

    ALLOWED_FILE_EXTENSIONS: list[str] = [".txt", ".log", ".pdf", ".doc", ".docx"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
