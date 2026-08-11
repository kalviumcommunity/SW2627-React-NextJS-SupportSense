from typing import List

# Default primary segmentation column
DEFAULT_SEGMENT_COLUMN: str = "customer_type"

# Minimum required columns for analysis
REQUIRED_COLUMNS: List[str] = [
    "customer_id",
    "lifetime_value",
    "churn",
    "support_tickets",
    "retention_days"
]

# Statistical sample size warning threshold
SMALL_SAMPLE_THRESHOLD: int = 30
