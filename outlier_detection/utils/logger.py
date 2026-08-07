import logging
import sys
from pathlib import Path
from outlier_detection.config.settings import DEFAULT_LOG_FILE

def setup_logger(name: str = "outlier_detection", log_file: Path = DEFAULT_LOG_FILE) -> logging.Logger:
    """
    Configures and returns a professional logger.
    Writes log statements to both console (stdout) and a log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicating handlers if they already exist
    if logger.handlers:
        return logger

    # Ensure parent log directories exist
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler (directed to stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
