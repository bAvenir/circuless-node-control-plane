import logging
import sys
import json
import os
from datetime import datetime
from typing import Any, Dict
from contextvars import ContextVar
from utils.config import settings

# Context variable to store request ID across async calls
request_id_var: ContextVar[str] = ContextVar('request_id', default='')


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format for easy parsing by FluentBit
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add request ID if available
        request_id = request_id_var.get()
        if request_id:
            log_data["request_id"] = request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from the log record
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """
    Configure application logging with structured JSON output
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(f"circuless_node.{settings.CLIENT_ID}")
    logger.setLevel(getattr(logging, settings.LOGS_LEVEL.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with structured formatting
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setFormatter(StructuredFormatter())
    # logger.addHandler(console_handler)
    
    # File handlers for verbose logs
    # Persistance to file
    # Fluent-bit picks up relevant logs and sends to LOKI (If configured)
    if settings.LOGS_EXTERNAL_ENABLED:
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Error log handler - captures ERROR and CRITICAL only
        file_handler = logging.FileHandler(
            os.path.join(log_dir, settings.LOGS_FILE_PATH),
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def log_with_context(logger: logging.Logger, level: str, message: str, **kwargs):
    """
    Helper function to log with additional context
    
    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **kwargs: Additional fields to include in the log
    """
    log_func = getattr(logger, level.lower())
    
    # Create a log record with extra fields
    extra_record = type('obj', (object,), {'extra_fields': kwargs})()
    log_func(message, extra={'extra_fields': kwargs})


# Initialize the logger
logger = setup_logging()