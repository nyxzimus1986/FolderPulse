"""
Logging Utilities
Centralized logging configuration for the application.
"""

import logging
import logging.handlers
from pathlib import Path
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Set up a logger with file and/or console output.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        console: Whether to log to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get an existing logger by name."""
    return logging.getLogger(name)


class LogCapture:
    """Context manager for capturing log output."""
    
    def __init__(self, logger_name: str, level: str = "INFO"):
        """
        Initialize log capture.
        
        Args:
            logger_name: Name of logger to capture
            level: Minimum level to capture
        """
        self.logger_name = logger_name
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.captured_logs = []
        self.handler = None
    
    def __enter__(self):
        """Start capturing logs."""
        self.handler = logging.Handler()
        self.handler.setLevel(self.level)
        self.handler.emit = self._capture_log
        
        logger = logging.getLogger(self.logger_name)
        logger.addHandler(self.handler)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop capturing logs."""
        if self.handler:
            logger = logging.getLogger(self.logger_name)
            logger.removeHandler(self.handler)
    
    def _capture_log(self, record):
        """Capture a log record."""
        self.captured_logs.append(record)
    
    def get_logs(self) -> list:
        """Get captured log records."""
        return self.captured_logs
    
    def get_messages(self) -> list:
        """Get captured log messages."""
        return [record.getMessage() for record in self.captured_logs]


# Initialize default logger
default_logger = setup_logger(
    "folderpulse",
    level="INFO",
    log_file="logs/app.log",
    console=True
)
