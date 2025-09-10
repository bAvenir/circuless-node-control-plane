from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    APP_NAME: str = "FastAPI Microservice"
    APP_VERSION: str = "0.0.1"
    APP_PORT: int = 3000
    APP_ENV: str = "DEV"
    DATABASE_URL: str
    START_UP_SECRET: str

    @property
    def SQL_LOG(self) -> bool:
        return self.APP_ENV.upper() == "DEV" 

settings = Settings()
