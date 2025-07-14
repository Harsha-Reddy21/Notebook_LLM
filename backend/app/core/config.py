import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, validator, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Notebook LLM"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database configuration
    DATABASE_URL: str = "sqlite:///./notebook_llm.db"
    
    # Vector database configuration
    VECTOR_DB_PATH: str = "./vector_db"
    
    # LLM configuration
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Document storage
    DOCUMENT_STORAGE_PATH: str = "./document_storage"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

# Debug print to check if OpenAI API key is loaded
print(f"OpenAI API Key loaded: {bool(settings.OPENAI_API_KEY)}")
if not settings.OPENAI_API_KEY:
    print("WARNING: OpenAI API Key is not set. LLM functionality will not work.") 