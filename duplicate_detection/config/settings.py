import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Ensure output and log directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration defaults
DEFAULT_DUPLICATE_KEYS = ["customer_id", "email"]

# Allowed strategies: "keep_first", "keep_last", "keep_most_complete"
VALID_STRATEGIES = ["keep_first", "keep_last", "keep_most_complete"]
DEFAULT_STRATEGY = "keep_first"

# Audit and report file paths
AUDIT_FILE_PATH = OUTPUT_DIR / "removed_duplicates_audit.csv"
REPORT_FILE_PATH = OUTPUT_DIR / "deduplication_report.json"
CLEANED_DATA_PATH = OUTPUT_DIR / "cleaned_customers.csv"
