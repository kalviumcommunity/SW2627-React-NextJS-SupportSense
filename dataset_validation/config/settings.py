import json
from pathlib import Path
from typing import Dict, Any, List

class Settings:
    """
    Configuration settings for the Dataset Validation module.
    """
    SUPPORTED_FORMATS: List[str] = [".csv", ".json", ".xlsx"]
    
    # The default output directory for validation reports
    REPORTS_DIR: Path = Path(__file__).resolve().parent.parent / "reports"
    
    # The default schema columns to validate against if no schema is provided.
    # In a production system, this could be loaded dynamically per dataset.
    DEFAULT_EXPECTED_SCHEMA: List[str] = [
        "ticket_id",
        "customer_name",
        "issue_type",
        "priority",
        "status",
        "created_at",
        "resolution_time_hrs",
        "satisfaction_score"
    ]
    
    @classmethod
    def ensure_directories(cls):
        """Ensures that required directories exist."""
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
