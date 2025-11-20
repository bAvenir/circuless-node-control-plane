from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    APP_NAME: str = "CIRCULess Node Control Plane"
    APP_VERSION: str = "0.0.1"
    APP_PORT: int = 8000
    APP_ENV: str = "DEV"
    APP_DIRECTORY: str = "LOCAL" # WOT directory implementation [LOCAL, WOT (UPMs)]
    APP_ONLINE: bool = False
    APP_CERTIFICATE_PATH: str = "certificate.pem"
    APP_CERTIFICATE: dict = {}
    APP_MODE: str = "SHARED" # App allows users of one or multiple organisations [ SHARED, PRIVATE]
    # CLOUD_SECRET: str = None # Cloud initialization secret
    CATALOGUE_URL: str = None
    # CONTRACT_MGR_URL: str = None
    AUTH_URL: str = None
    AUTH_REALM: str = "circuless"
    # Loaded from certificate (IF NONE, collaborative features disabled)
    CLIENT_ID: str = ""
    # Database info
    DATABASE_URL: str = "postgresql+asyncpg://bavenir:bavenir@localhost:5432/circdb"
    DATABASE_TABLE: str = os.getenv("DATABASE_TABLE", "items")
    # OTEL
    OTEL_EXPORTER: str = "zipkin" # TBD configure more exporters
    OTEL_ENDPOINT: str = "http://localhost:9411/api/v2/spans"
    OTEL_ENABLED: bool = True
    # LOGGER
    LOGS_FILE_PATH: str = "app.log"
    LOGS_EXTERNAL_ENABLED: bool = True
    LOGS_LEVEL: str = "ERROR" # (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    @property
    def SQL_LOG(self) -> bool:
        return self.APP_ENV.upper() == "DEV"

settings = Settings()
