from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Code-Share"
    DEBUG: bool = True
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    DATABASE_URL: str = f"sqlite:///{os.path.join(DATA_DIR, 'codeShare.db')}"
    API_PORT: int = 3000
    API_HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 