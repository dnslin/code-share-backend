from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Code-Share"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./codeShare.db"
    API_PORT: int = 3000
    API_HOST: str = "0.0.0.0"

settings = Settings() 