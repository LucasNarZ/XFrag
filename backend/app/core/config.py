from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    session_cookie_name: str = "session_token"
    session_ttl_seconds: int = 86400
    session_cookie_secure: bool = False
    session_cookie_samesite: str = "lax"

    model_config = {
        "env_file": Path(__file__).resolve().parent.parent.parent.parent / ".env",
        "extra": "ignore",
    }


settings = Settings()
