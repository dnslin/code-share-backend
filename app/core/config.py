from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Code-Share"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./codeShare.db"
    API_PORT: int = 3000
    API_HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 