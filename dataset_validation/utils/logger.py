import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = "dataset_validation.log") -> logging.Logger:
    """
    Configures and returns a professional logger.
    Logs are written to both the console (stdout) and a log file.
    
    Args:
        name (str): The name of the logger, typically __name__.
        log_file (str): The name of the log file.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_path = log_dir / log_file
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if logger is initialized multiple times
    if logger.handlers:
        return logger
        
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # File Handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
