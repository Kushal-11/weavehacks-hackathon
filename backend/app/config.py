from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Keys
    EXA_API_KEY: str = ""
    WANDB_API_KEY: str = ""
    OPENAI_API_KEY: str = ""  # Fallback for LLM
    
    # Database
    REDIS_URL: str = "redis://localhost:6379"
    POSTGRES_URL: str = "postgresql://user:pass@localhost/memewars"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Game Settings
    ROUND_DURATION: int = 90  # seconds
    ROUNDS_PER_GAME: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings() 