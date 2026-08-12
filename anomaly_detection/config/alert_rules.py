from typing import Dict, Any

# Threshold-based business alert rules
ALERT_RULES: Dict[str, Dict[str, Any]] = {
    "daily_revenue": {
        "min": 2000,   # Revenue below this triggers a BELOW_MIN (HIGH severity) alert
        "max": 30000   # Revenue above this triggers an ABOVE_MAX (MEDIUM severity) alert
    }
}

# Configuration for Statistical Detection
LOOKBACK_DAYS = 30
ZSCORE_ANOMALY_THRESHOLD = 2.0
