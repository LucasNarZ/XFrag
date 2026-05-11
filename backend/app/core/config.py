from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str 
    session_cookie_name: str = "session_token"
    session_ttl_seconds: int = 86400
    session_cookie_secure: bool = False
    session_cookie_samesite: str = "lax"

    model_config = {
        "env_file": Path(__file__).resolve().parent.parent.parent.parent / ".env",
        "extra": "ignore",
    }


settings = Settings()
