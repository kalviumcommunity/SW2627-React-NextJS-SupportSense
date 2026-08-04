"""
Centralized logging utility for the Dataset Profiling Framework.
Provides consistent logging configuration and standard output formats.
"""

import logging
import sys
from pathlib import Path

def get_logger(module_name: str) -> logging.Logger:
    """
    Configures and returns a logger with the specified module name.
    Logs to both console and a log file in the reports/logs directory.
    
    Args:
        module_name (str): The name of the module (usually __name__).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(module_name)
    
    # Avoid adding multiple handlers if the logger is already configured
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    # Ensure logs directory exists
    log_dir = Path("dataset_profiling/reports/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(
        filename=log_dir / "profiler.log",
        mode="a",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
