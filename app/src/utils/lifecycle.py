from .config import settings
from .logs import get_logger

logger=get_logger(__name__)

def initialize():
    logger.info("Welcome to CIRCULess node app")
    logger.info(f"Running on version {settings.APP_VERSION} ... ")
    logger.info(f"Running in {settings.APP_ENV} mode")
    # Load certificates
    # Handshake with cloud (Publish )
    return
    
def shutdown():
    return
