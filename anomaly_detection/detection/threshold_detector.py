import logging
import pandas as pd
from typing import Dict, Any, List

logger = logging.getLogger("anomaly_detection.detection.threshold_detector")

def check_thresholds(df: pd.DataFrame, metric_col: str, rules: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Checks the metric against statically configured business thresholds (min/max).
    Generates threshold alerts.
    """
    logger.info(f"Checking threshold rules for '{metric_col}'.")
    alerts = []
    
    if metric_col not in rules:
        logger.info(f"No threshold rules configured for metric '{metric_col}'.")
        return alerts
        
    rule = rules[metric_col]
    min_val = rule.get("min")
    max_val = rule.get("max")
    
    for _, row in df.iterrows():
        val = row[metric_col]
        date_str = row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else "Unknown Date"
        
        direction = None
        severity = None
        threshold_val = None
        
        if min_val is not None and val < min_val:
            direction = "BELOW_MIN"
            severity = "HIGH"
            threshold_val = min_val
        elif max_val is not None and val > max_val:
            direction = "ABOVE_MAX"
            severity = "MEDIUM"
            threshold_val = max_val
            
        if direction:
            alerts.append({
                "timestamp": pd.Timestamp.utcnow().isoformat(),
                "anomaly_date": date_str,
                "metric": metric_col,
                "value": val,
                "mean": None,
                "standard_deviation": None,
                "expected_range": f"{min_val if min_val is not None else '-inf'} to {max_val if max_val is not None else 'inf'}",
                "z_score": None,
                "severity": severity,
                "detection_method": f"THRESHOLD ({direction} {threshold_val})",
                "status": "OPEN"
            })
            
    logger.info(f"Detected {len(alerts)} threshold anomalies for '{metric_col}'.")
    return alerts
