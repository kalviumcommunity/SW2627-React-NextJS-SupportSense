import logging
import sys
from pathlib import Path
from duplicate_detection.config.settings import LOGS_DIR

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up an enterprise-grade logger.
    Logs both to console (stdout) and file.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding duplicate handlers if they are already setup
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console Handler (directed to stdout)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File Handler
        fh = logging.FileHandler(LOGS_DIR / "duplicate_detection.log", encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
