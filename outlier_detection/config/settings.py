import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Default Pipeline Configurations
DEFAULT_DETECTION_METHOD = "zscore"  # Supported: "zscore", "iqr"
DEFAULT_HANDLING_STRATEGY = "flag"  # Supported: "cap", "remove", "flag"

# Default Statistical Parameters
DEFAULT_Z_SCORE_THRESHOLD = 3.0
DEFAULT_IQR_MULTIPLIER = 1.5

# File Output Settings
AUDIT_LOG_FILE = OUTPUT_DIR / "outlier_cleaning_log.csv"
REPORT_JSON_FILE = OUTPUT_DIR / "outlier_report.json"
DEFAULT_LOG_FILE = LOG_DIR / "outlier_detection.log"
