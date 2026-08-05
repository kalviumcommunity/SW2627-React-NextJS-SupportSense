import logging
import sys
from pathlib import Path
from data_type_enforcement.config.settings import LOGS_DIR

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up an enterprise-grade logger.
    Logs both to console (stdout) and file.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File Handler
        fh = logging.FileHandler(LOGS_DIR / "type_enforcement.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
