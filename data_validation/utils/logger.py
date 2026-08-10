import logging
import sys
from pathlib import Path

def setup_logger(name: str = "data_validation", log_dir: str = "logs") -> logging.Logger:
    """
    Sets up and returns a professional logger.
    Logs to console and a local application log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicating handlers if already set up
    if logger.handlers:
        return logger

    # Ensure parent log directories exist
    log_path = Path(log_dir) / "data_validation.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

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
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
