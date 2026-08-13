import logging
import sys

def setup_logger(name: str = "sql_joins") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(message)s")
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def extract_queries(sql_file: str) -> list:
    """Reads a .sql file and splits it into individual queries."""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by semicolon and remove empty queries
    queries = [q.strip() for q in content.split(';') if q.strip()]
    return queries
