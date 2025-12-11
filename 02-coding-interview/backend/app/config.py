from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", alias="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = Field(default="HS256", alias="ALGORITHM")
    DATABASE_URL: str = Field(default="sqlite:///./interview.db", alias="DATABASE_URL")
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
