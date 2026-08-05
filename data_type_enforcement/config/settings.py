import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Ensure output directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration for boolean conversion
BOOLEAN_MAPPING = {
    "1": True,
    "0": False,
    "true": True,
    "false": False,
    "yes": True,
    "no": False,
    "y": True,
    "n": False,
    "t": True,
    "f": False
}

# Configuration for currency cleaning
CURRENCY_SYMBOLS = ["$", "₹", "€", "£", ","]

# Default expected schema mapping for the dataset
# A typical structure looks like:
# "column_name": {"type": "date", "format": "%Y-%m-%d"} or {"type": "currency"} or {"type": "boolean"} or {"type": "string"} or {"type": "int"}
DEFAULT_SCHEMA = {
    "id": {"type": "int"},
    "name": {"type": "string"},
    "signup_date": {"type": "date", "format": "%Y-%m-%d"},
    "is_active": {"type": "boolean"},
    "balance": {"type": "currency"},
    "last_login": {"type": "date", "format": "%Y/%m/%d %H:%M:%S"}
}
